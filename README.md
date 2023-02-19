# Video Uploader
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/OmarNunezG/video-uploader/checks.yml?label=Checks&logo=github&style=for-the-badge)
![GitHub Contributors](https://img.shields.io/github/contributors/OmarNunezG/video-uploader?logo=github&style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/OmarNunezG/video-uploader?logo=github&style=for-the-badge)
![GitHub Release Date](https://img.shields.io/github/release-date/OmarNunezG/video-uploader?logo=github&style=for-the-badge)

## Table of Contents
- [Video Uploader](#video-uploader)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Requirements](#requirements)
    - [Python](#python)
  - [Features](#features)
  - [Video Requirements](#video-requirements)
  - [Database schema](#database-schema)
  - [Getting started](#getting-started)
  - [API documentation](#api-documentation)
    - [Swagger](#swagger)
    - [Postman](#postman)
  - [Usage](#usage)
  - [Authentication and authorization](#authentication-and-authorization)
  - [Testing](#testing)
  - [Admin site](#admin-site)
  - [License](#license)

## Description
This is a Django REST Framework (DRF) web API for uploading and managing videos. It provides endpoints for CRUD operations on video files, comments and users. Additionally, it includes authentication and authorization features using JSON Web Tokens (JWT) and supports Cross-Origin Resource Sharing (CORS) using django-cors-headers.

Resources are paginated and can be sorted, filtered and searched. Videos can be tagged and users can like videos, comments and replies. Replies can also be liked.

Endpoints are available for users to register, login, change their password, reset their password and manage their account. The API also provides endpoints for users to manage their videos, comments and likes.

The API documentation is generated using [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/).

Most endpoints are protected and require authentication. To access protected endpoints, you must include a valid JWT token in the `Authorization` header of your request. The token must be prefixed with `Bearer `.

To get a JWT token, you must first register a user account. Once you have registered an account, you can login to get a JWT token. You can then use the token to access protected endpoints.

For more information about authentication and authorization, see the [Authentication and Authorization](#authentication-and-authorization) section.

Read the [API documentation](#api-documentation) to learn more about the endpoints.

## Requirements
### Python
This project requires Python 3.10.10 or higher. You can download Python from [python.org](https://www.python.org/downloads/).

The following Python packages are required:
| Package                       | Version |
| ----------------------------- | ------- |
| Django                        | 4.1.7   |
| django-cors-headers           | 3.13.0  |
| django-environ                | 0.9.0   |
| djangorestframework           | 3.14.0  |
| djangorestframework-simplejwt | 5.2.2   |
| drf_spectacular               | 0.25.1  |
| Pillow                        | 9.4.0   |

## Features
This project provides a number of features to help users upload and manage their video files. Some of the key features include:

- API documentation
- Comment likes
- Comment replies
- Comment reply likes
- Cross-Origin Resource Sharing (CORS) support
- Django admin site
- Pagination
- Password change
- Password reset
- Password validation
- Search and filtering
- Sorting
- User authentication and authorization using JWT tokens
- User management
- User registration
- Video comments
- Video likes
- Video tags
- Video upload and management

## Video Requirements
- Must be in mp4 format
- Must have a title
- Should have a description
- Must have a thumbnail
- Should have tags
- Must be shorter than 10 minutes
- Must be less than 100 MB

## Database schema
![Database schema](docs/images/database%20schema.png)

## Getting started
To get started with this project, follow these steps:

1. Clone the repository
   - HTTPS
   ```bash
   $ git clone https://github.com/yezyilomo/django-restql.git
   ```
   - SSH
   ```bash
   $ git clone git@github.com:yezyilomo/django-restql.git
   ```
   - GitHub CLI
   ```bash
   $ gh repo clone yezyilomo/django-restql
   ```
2. Create a virtual environment:
   ```bash
   $ python -m venv env
   ```
3. Activate the virtual environment:
    - Windows
    ```bash
    $ env\Scripts\activate
    ```
    - Linux / MacOS
    ```bash
    $ source env/bin/activate
    ```
4. Install the dependencies:
    ```bash
    $ pip install -r requirements.txt
    ```
5. Create a `.env` file in the app project directory and add the following environment variables:
    ```
    # Django settings
    SECRET_KEY=<your-secret-key>
    DEBUG=<True|False>

    # Database settings
    DATABASE_ENGINE=<your-db-engine>
    DATABASE_NAME=<your-db-name>
    DATABASE_USER=<your-db-user>
    DATABASE_PASSWORD=<your-db-password>
    DATABASE_HOST=<your-db-host>
    DATABASE_PORT=<your-db-port>
    ```
    - Replace `<your-secret-key>` with a secret key for your project. You can generate one using [Djecrety](https://djecrety.ir/).
    - Replace `<your-db-engine>`, `<your-db-name>`, `<your-db-user>`, `<your-db-password>`, `<your-db-host>`, and `<your-db-port>` with the appropriate values for your database.

    For the `DB_ENGINE` variable, you can use `django.db.backends.postgresql` for PostgreSQL or `django.db.backends.sqlite3` for SQLite.
6. Run the migrations:
    ```bash
    $ python manage.py migrate
    ```
7. Create a superuser:
    ```bash
    $ python manage.py createsuperuser
    ```
    Follow the prompts to create a superuser.
1. Run the development server:
    ```bash
    $ python manage.py runserver
    ```
    The development server will be available at `http://localhost:8000/` and `http://127.0.0.1:8000/`.

## API documentation
This project provides API documentation using Swagger and Postman.

### Swagger
To view the API documentation using Swagger, open the Swagger documentation at `http://localhost:8000/api/swagger/` or `http://127.0.0.1:8000/api/swagger/` in your browser.

### Postman
To view the API documentation using Postman, import the `postman_collection.json` file into Postman.

To get the Postman collection, follow these steps:

1. Click on `/api/schema/` in the Swagger documentation.
2. Click on `Import` in the top left corner.
3. Import the JSON file into Postman.

## Usage
This API uses RESTful endpoints. The documentation is generated using [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/).

For example, the endpoint for creating a new user is called `POST /api/users/`. The endpoint accepts a JSON object with the following structure:
```json
{
  "data": {
    "type": "users",
    "attributes": {
      "first_name": "Michael",
      "middle_name": null,
      "last_name": "Scott",
      "username": "michael.scott",
      "email": "michaelstt@example.com",
      "password": "s3cr3tp@ssw0rd"
    }
  }
}
```

If the user is created successfully, a `201 status code` is going to be returned, as well as a Location header including it's absolute path and a JSON object.

The Location header will look like this:
```bash
Location: http://localhost:8000/api/users/1
```

The JSON object will look like this:
```json
{
  "data": {
    "id": "1",
    "type": "users",
    "attributes": {
      "first_name": "Michael",
      "middle_name": null,
      "last_name": "Scott",
      "username": "michael.scott",
      "email": "michaelstt@example.com",
    },
    "relationships": {
      "videos": {
        "links": {
          "self": "/api/users/1/relationships/videos",
          "related": "/api/users/1/videos"
        },
        "data": []
      }
    },
    "links": {
      "self": "/api/users/1"
    }
  }
}
```

If the username is already in use, a `409 status code` is going to be returned, as well as a JSON object with the following structure:
```json
{
  "errors": [
    {
      "status": "409",
      "title": "Conflict",
      "detail": "The username 'michael.scott' is already in use.",
      "source": {
        "pointer": "/data/attributes/username"
      }
    }
  ]
}
```

## Authentication and authorization
This API uses [JSON Web Tokens](https://jwt.io/) for authentication and authorization. To authenticate a user, follow these steps:

1. Create a new user using the `POST /api/users/` endpoint.
2. Login using the `POST /api/token/` endpoint.
3. Copy the access token from the response.
4. Add the access token to the `Authorization` header of the request.

## Testing
To run the tests run the following command:
```bash
$ python manage.py test
```

To run a specific test, run the following command:
```bash
$ python manage.py test <app_name>
```

## Admin site
This site provides a user interface for managing the data in the database. To access the admin site, follow these steps:

1. Open the admin site at `http://localhost:8000/admin/` or `http://127.0.0.1:8000/admin/` in your browser.
2. Login with the superuser credentials you created on step 7 of the [Getting started](#getting-started) section.

## License
This project is licensed under the Unlicense. See the [LICENSE](LICENSE) file for details.
