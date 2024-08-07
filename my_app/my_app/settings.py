import os
from pathlib import Path
from os import environ

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = int(os.environ.get('DEBUG', default=0))
#DEBUG = True

#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.sitemaps',
    "captcha",

    "home.apps.HomeConfig",


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'my_app.context_processors.active_nav',

            ],
        },
    },
]

WSGI_APPLICATION = 'my_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
#
DATABASES = {
    'default': {
        'ENGINE': environ.get('POSTGRES_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': environ.get('POSTGRES_DB', BASE_DIR / 'db.sqlite3'),
        'USER': environ.get('POSTGRES_USER', 'user'),
        'PASSWORD': environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': environ.get('POSTGRES_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# #


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#AUTH_USER_MODEL = 'account.User'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']






CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': os.path.join(BASE_DIR, 'app_caches'),
#     }
# }
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',

    }
}


SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'my_app_session_id'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 3600  # время в секундах 1 час

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'  # SMTP Mail.ru
EMAIL_PORT = 465
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


LOGGING = {
    "version": 1,
    "handlers": {
        "console": {'class': 'logging.StreamHandler'}
    },
    "loggers": {
        'django.contrib.auth.backends.ModelBackend': {
            "handlers": ['console'],
            'level': 'ERROR'
        }
    }
}

SITE_ID = 1