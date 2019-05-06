"""
Django settings for Linuxjobber project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, sys, datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from decouple import config, Csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'y@my*7-t9p1rzf&2ryw*m+@1w-*-e5d=)5l_9)5ibtw7v7#2z_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [

    'rest_framework',
    # 'djstripe',
    'channels',
    'ckeditor',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    # 'home.apps.HomeConfig',
    'home',
    'Courses.apps.CoursesConfig',
    'Projects.apps.ProjectsConfig',
    'ToolsApp.apps.ToolsappConfig',
    'classroom.apps.ClassroomConfig',
    'rest_framework.authtoken',
    'sso_api'
]

CORS_ORIGIN_ALLOW_ALL = True

# Default permission that allows anyone to access our API. This is left this way for development purpose it should be changed before it gets to production.

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'classroom.views.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=24),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Linuxjobber.urls'

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
                'home.context_processors.courses',
                'home.context_processors.tools',
                'home.context_processors.workexperience',
            ],
        },
    },
]

WSGI_APPLICATION = 'Linuxjobber.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Todo Before Push modify to original credentials
# Here I made use of a mysql database for expense application
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME', 'linuxjobber'),  # linuxjb
        'USER': config('DATABASE_USER', 'root'),  # linuxjobber
        'PASSWORD': config('DATABASE_PASSWORD', ''),  # linuxjobber
        'HOST': config('DATABASE_HOST', 'localhost'),
        'PORT': config('DATABASE_PORT', '3306'),

    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S'
        },

        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },

        'development_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_dev.log'),
            'formatter': 'verbose'
        },

        'production_logfile': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'django_production.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'simple'
        },

        'dba_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_false', 'require_debug_true'],
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'django_dba.log'),
            'formatter': 'simple'
        },
    },

    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },

    'loggers': {
        'livelinuxjobber': {
            'handlers': ['development_logfile', 'production_logfile'],
        },

        'dba': {
            'handlers': ['dba_logfile'],
        },

        'django': {
            'handlers': ['development_logfile', 'production_logfile'],
        },

        'py.warnings': {
            'handlers': ['development_logfile'],
        },
    }
}

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'asset'),
)

# STATIC_ROOT = os.path.join(BASE_DIR, 'asset')

# CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home'

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
ENV_URL = "http://127.0.0.1:8000/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST', 'smtp.linuxjobber.com')
EMAIL_PORT = config('EMAIL_PORT', '587')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', 'admin@linuxjobber.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', 'm4k3Aw!y')
EMAIL_USE_TLS = True

STRIPE_PUBLIC_KEY = "pk_test_w1kMWsWp53qxIwH2XHedu9co00waZwHxdJ"
STRIPE_SECRET_KEY = "Something"
AUTH_USER_MODEL = 'users.CustomUser'



STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "")
STRIPE_LIVE_MODE = False
DJSTRIPE_WEBHOOK_SECRET = "whsec_3o62zcRDbp7X4tpJa7BYHztqK6rbKoSv"

# Channels
ASGI_APPLICATION = 'Linuxjobber.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [config('channel_hosts', default="127.0.0.1,6379", cast=Csv(post_process=tuple))],
        },
    },
}

# todo Always change to appropriate before pushing
# SERVER details
SERVER_IP = config('SERVER_IP', "192.168.122.1")
SERVER_USER = config('SERVER_USER', "sysadmin")
SERVER_PASSWORD = config('SERVER_PASSWORD', "8iu7*IU&")
GROUP_CLASS_URL = config('GROUP_CLASS_URL', 'http://localhost:4200/classroom/')

# Session Expiration set to 10 mins
SESSION_COOKIE_AGE = 60 * 60


