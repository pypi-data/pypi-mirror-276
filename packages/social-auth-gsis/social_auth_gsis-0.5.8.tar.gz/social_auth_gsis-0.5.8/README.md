# Social Auth GSIS

[Python Social Auth](https://python-social-auth.readthedocs.io/en/latest/) backend for the OAuth 2.0 for [GSIS](https://gsis.gr/en), intended for use in [Django applications](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html).

## Requirements

- Python 3.8, or newer
- Django 3.2, or newer

## Installation

Install the [`social-auth-gsis` from PyPI](https://pypi.org/project/social-auth-gsis/) using your favorite package manager.

### pip

```console
pipi install social-auth-gsis
```

### Poetry

```console
poetry add social-auth-gsis
```

## Usage

To get the GSIS authentication package working with a Django application, both settings and URLs need to be configured.

### Settings

The best place to get started with integrating Social Auth GSIS in a Django project is the settings.

First, the `social_django` app needs to be added in the [`INSTALLED_APPS`](https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-INSTALLED_APPS) setting of your Django application:

```py
INSTALLED_APPS = [
    # ...the rest of installed apps
    "social_django",
]
```

Next, `social_django.middleware.SocialAuthExceptionMiddleware` needs to be included in [`MIDDELWARE`](https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-MIDDLEWARE), right below the `django.middleware.clickjacking.XFrameOptionsMiddleware`:

```py
MIDDLEWARE = [
    # ...the rest of middleware
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]
```

In order to only allow creation of users through the social auth pipeline, the [`SOCIAL_AUTH_PIPELINE`](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html#personalized-configuration) Django Social Auth setting needs to be set to the following value:

```py
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_auth_gsis.pipeline.social_auth.social_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
```

To configure the credentials and redirect URLs of a Social Auth GSIS backend the appropriate settings need to be set as well:

```py
SOCIAL_AUTH_GSIS_KEY = "oauth2_client_key"
SOCIAL_AUTH_GSIS_SECRET = "oauth2_client_secret"
SOCIAL_AUTH_GSIS_REDIRECT_URL = "https://yourapp.local/authorize/gsis/"
```

Finally, the intended backends should be included in the [`AUTHENTICATION_BACKENDS`](https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-AUTHENTICATION_BACKENDS) setting:

```py
AUTHENTICATION_BACKENDS = (
    "social_auth_gsis.backends.GSISOAuth2",
    # ...the rest of backends included
)
```

### URLs

The URLs of Django Social Auth are required to be included also, in order to authenticate users redirected from GSIS' auth:

```py
from django.urls import include, path
from social_django import views as social_django_views


urlpatterns = [
    path("auth/", include("social_django.urls", namespace="social")),
    # ...the rest of URL patterns
]
```

The ability to explicitly set the backend to be used in a URL for authentication, is also possible:

```py
urlpatterns = [
    path(
        "authorize/gsis/",
         social_django_views.complete,
        kwargs={"backend": "ktimatologio_gsis"},
        name="authorize",
    ),
    # ...the rest of URL patterns
]
```

## Backends

The following social auth backends are available in `social_auth_gsis.backends`.

### `GSISOAuth2`

Used for authentication of citizens. For testing purposes the `GSISOAuth2Testing` backend should be used instead. The following settings are required:

- `SOCIAL_AUTH_GSIS_KEY`
- `SOCIAL_AUTH_GSIS_SECRET`
- `SOCIAL_AUTH_GSIS_REDIRECT_URL`

### `GSISOTPOAuth2`

Used for authentication of citizens, requiring also OTP verification. For testing purposes the `GSISOTPOAuth2Testing` backend should be used instead. The following settings are required:

- `SOCIAL_AUTH_GSIS_OTP_KEY`
- `SOCIAL_AUTH_GSIS_OTP_SECRET`
- `SOCIAL_AUTH_GSIS_OTP_REDIRECT_URL`

### `GSISPAOAuth2`

Used for authentication of public sector employees (PA for Public Administration). For testing purposes the `GSISPAOAuth2Testing` backend should be used instead. The following settings are required:

- `SOCIAL_AUTH_GSIS_PA_KEY`
- `SOCIAL_AUTH_GSIS_PA_SECRET`
- `SOCIAL_AUTH_GSIS_PA_REDIRECT_URL`
