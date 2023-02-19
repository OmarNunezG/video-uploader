from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class VideoTagInline(admin.TabularInline):
    model = models.VideoTag
    extra = 0
    verbose_name = "Tag"
    verbose_name_plural = "Tags"


class UserAdmin(BaseUserAdmin):
    ordering = ("id",)
    list_display = ("username", "email", "date_joined")
    fieldsets = (
        (
            "Personal info",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "username",
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            "Others",
            {
                "classes": ("wide",),
                "fields": ("last_login",),
            },
        ),
    )
    readonly_fields = ("last_login",)
    add_fieldsets = (
        (
            "Personal info",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


class VideoAdmin(ModelAdmin):
    ordering = ("id",)
    list_display = ("title", "description", "created_by", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "created_by__username")
    fieldsets = (
        (
            "Content",
            {
                "classes": ("wide",),
                "fields": (
                    "title",
                    "description",
                    "thumbnail",
                    "file",
                ),
            },
        ),
        (
            "Metadata",
            {
                "classes": ("wide",),
                "fields": (
                    "likes",
                    "created_by",
                    "created_at",
                ),
            },
        ),
    )
    readonly_fields = ("likes", "created_at")
    add_fieldsets = (
        (
            "Content",
            {
                "classes": ("wide",),
                "fields": (
                    "title",
                    "description",
                    "thumbnail",
                    "file",
                ),
            },
        ),
        (
            "Metadata",
            {
                "classes": ("wide",),
                "fields": (
                    "created_by",
                ),
            },
        ),
    )
    inlines = (VideoTagInline,)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ("created_by",)
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["initial"] = request.user.id
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CommentAdmin(ModelAdmin):
    ordering = ("id",)
    list_display = ("video", "text", "created_by", "created_at")
    list_filter = ("created_at",)
    search_fields = ("created_by__username",)
    readonly_fields = ("likes", "created_at")
    fieldsets = (
        (
            "Content",
            {
                "classes": ("wide",),
                "fields": ("text",),
            },
        ),
        (
            "Metadata",
            {
                "classes": ("wide",),
                "fields": (
                    "video",
                    "likes",
                    "created_by",
                    "created_at",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            "Content",
            {
                "classes": ("wide",),
                "fields": ("text",),
            },
        ),
        (
            "Metadata",
            {
                "classes": ("wide",),
                "fields": (
                    "video",
                    "created_by",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields += ("created_by",)
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["initial"] = request.user.id
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class VideoTagAdmin(ModelAdmin):
    ordering = ("id",)
    list_display = ("video", "tag", "get_created_by")
    fieldsets = (
        (
            "Content",
            {
                "classes": ("wide",),
                "fields": (
                    "video",
                    "tag",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("video",)
        return ()

    def get_created_by(self, obj):
        return obj.video.created_by

    get_created_by.short_description = "Video uploaded by"


class VideoLikeAdmin(ModelAdmin):
    ordering = ("id",)
    list_display = ("video", "get_created_by")
    fieldsets = (
        (
            "Content",
            {
                "classes": ("wide",),
                "fields": ("video", "liked_by"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("video", "liked_by")
        return ()

    def get_created_by(self, obj):
        return obj.video.created_by

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "liked_by":
            kwargs["initial"] = request.user.id
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.video.likes += 1
        obj.video.save()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.video.likes -= 1
        obj.video.save()
        super().delete_model(request, obj)

    get_created_by.short_description = "Video uploaded by"


class CommentLikeAdmin(ModelAdmin):
    ordering = ("id",)
    list_display = ("comment", "liked_by", "get_video")
    fieldsets = (
        (
            "Content",
            {
                "classes": ("wide",),
                "fields": (
                    "comment",
                    "liked_by",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("comment", "liked_by")
        return ()

    def get_video(self, obj):
        return obj.comment.video

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "liked_by":
            kwargs["initial"] = request.user.id
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.video.likes += 1
        obj.video.save()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.video.likes -= 1
        obj.video.save()
        super().delete_model(request, obj)

    get_video.short_description = "Video"


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Video, VideoAdmin)
