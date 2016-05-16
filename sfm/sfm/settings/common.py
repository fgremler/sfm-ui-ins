"""
Django settings for sfm project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import environ as env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$qjsxe%dh54l8x&#y2sj7=+hc=4$b9f1ujo7*77_n)__qx#up='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.get('SFM_DEBUG', 'True') == 'True'

# Host/domain names that this Django site can serve.
# Used when DEBUG = False
# See https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts
# This will remove ports if provided.
ALLOWED_HOSTS = (env.get('SFM_HOST', 'localhost').split(":")[0])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'ui',
    'allauth',                      # registration
    'allauth.account',              # registration
    'allauth.socialaccount',        # registration
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.weibo',
    'crispy_forms',                 # for django crispy forms
    'apscheduler',                  # Scheduler
    'message_consumer',             # Message Consumer
    'simple_history',
    'rest_framework',               # For REST API
    'api',
    'datetimewidget'
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

ROOT_URLCONF = 'sfm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sfm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sfmdatabase',
        'USER': 'postgres',
        'PASSWORD': env.get('DB_ENV_POSTGRES_PASSWORD'),
        'HOST': env.get('DB_ENV_HOST', 'db'),
        'PORT': '5432',
    }
}

SCHEDULER_DB_URL = "postgresql://{USER}:{PASSWORD}@{HOST}/{NAME}".format(**DATABASES["default"])

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env.get('CONTAINER_TIMEZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

LOGIN_REDIRECT_URL = "/"

# Authentication Backends for AllAuth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

# Required due to custom fields on AbstractUser, see "Substituting
# a custom user model" under:
# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/
AUTH_USER_MODEL = 'ui.User'

SOCIALACCOUNT_STORE_TOKENS = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_ADAPTER = "ui.auth.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "ui.auth.SocialAccountAdapter"

RABBITMQ_HOST = env.get('SFM_RABBITMQ_HOST')
RABBITMQ_USER = env.get('SFM_RABBITMQ_USER')
RABBITMQ_PASSWORD = env.get('SFM_RABBITMQ_PASSWORD')

# crispy forms bootstrap version
CRISPY_TEMPLATE_PACK = 'bootstrap3'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

# Directory where SFM data (e.g., harvested WARCs) is stored.
SFM_DATA_DIR = env.get("SFM_DATA_DIR", "/sfm-data")

# Whether to register receivers on SeedSet for scheduling harvests.
SCHEDULE_HARVESTS = True

# Whether to register receivers on Export for performing exports.
PERFORM_EXPORTS = True

# Add a 5 minute schedule interval. This is useful for dev and testing.
FIVE_MINUTE_SCHEDULE = env.get('SFM_FIVE_MINUTE_SCHEDULE', 'False') == 'True'

# Whether to send emails.
PERFORM_EMAILS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.get('SFM_SMTP_HOST', 'smtp.gmail.com')
EMAIL_PORT = 587
EMAIL_HOST_USER = env.get('SFM_EMAIL_USER')
EMAIL_HOST_PASSWORD = env.get('SFM_EMAIL_PASSWORD')
EMAIL_USE_TLS = True
