from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class MaxSizeValidator(BaseValidator):
    message = "File size exceeded."
    code = "file_size_exceeded"

    def __init__(self, max_size, message=None, code=None):
        self.max_size = max_size
        super().__init__(message, code)

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(self.message, code=self.code)
