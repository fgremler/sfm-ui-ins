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
from django.conf.locale.en import formats as sfm_formats

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
ALLOWED_HOSTS = (env.get('SFM_HOST', 'localhost').split(":")[0], 'api', 'ui')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'ui',
    'allauth',                      # registration
    'allauth.account',              # registration
    'allauth.socialaccount',        # registration
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.tumblr',
    'crispy_forms',                 # for django crispy forms
    'apscheduler',                  # Scheduler
    'message_consumer',             # Message Consumer
    'simple_history',
    'rest_framework',               # For REST API
    'django_filters',
    'api',
    'datetimewidget'
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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
                'ui.context_processors.settings',
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
        'PASSWORD': env.get('POSTGRES_PASSWORD'),
        'HOST': env.get('POSTGRES_HOST', 'db'),
        'PORT': '5432',
    }
}

SCHEDULER_DB_URL = "postgresql://{USER}:{PASSWORD}@{HOST}/{NAME}".format(**DATABASES["default"])

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env.get('TZ', "America/New_York")

USE_I18N = True

USE_L10N = True

USE_TZ = True

# https://docs.djangoproject.com/en/1.10/ref/settings/#datetime-format
# https://docs.djangoproject.com/en/1.10/ref/templates/builtins/#date
sfm_formats.DATETIME_FORMAT = "N j, Y, g:i:s a e"
DATETIME_FORMAT = "N j, Y, g:i:s a e"

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
RABBITMQ_MANAGEMENT_PORT = env.get('SFM_RABBITMQ_MANAGEMENT_PORT', "15672")

# crispy forms bootstrap version
CRISPY_TEMPLATE_PACK = 'bootstrap3'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 250
}

# Institution name, such as 'GW Libraries'
INSTITUTION_NAME = env.get('SFM_INSTITUTION_NAME')

# a link for the institution name, such as 'http://library.gwu.edu'
INSTITUTION_LINK = env.get('SFM_INSTITUTION_LINK')

# Directory where SFM data (e.g., harvested WARCs) is stored.
SFM_DATA_DIR = env.get("SFM_DATA_DIR", "/sfm-data")

# Directory where SFM processing data is stored.
SFM_PROCESSING_DIR = env.get("SFM_PROCESSING_DIR", "/sfm-processing")

# Whether to register receivers on Collection for scheduling harvests.
SCHEDULE_HARVESTS = True

# Whether to register receivers on Export for performing exports.
PERFORM_EXPORTS = True

# Add a 5 minute schedule interval. This is useful for dev and testing.
FIVE_MINUTE_SCHEDULE = env.get('SFM_FIVE_MINUTE_SCHEDULE', 'False') == 'True'

# Add a 100 item export segment. This is useful for dev and testing.
HUNDRED_ITEM_SEGMENT = env.get('SFM_HUNDRED_ITEM_SEGMENT', 'False') == 'True'

# Turn on or off the weibo search collection, default is turn off
WEIBO_SEARCH_OPTION = env.get('SFM_WEIBO_SEARCH_OPTION', 'False') == 'True'

# Whether to send emails.
PERFORM_EMAILS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.get('SFM_SMTP_HOST', 'smtp.gmail.com')
EMAIL_PORT = 587
EMAIL_HOST_USER = env.get('SFM_EMAIL_USER')
EMAIL_HOST_PASSWORD = env.get('SFM_EMAIL_PASSWORD')
EMAIL_USE_TLS = True

# contact email
CONTACT_EMAIL = env.get('SFM_CONTACT_EMAIL')

# Whether to run apscheduler
RUN_SCHEDULER = env.get('SFM_RUN_SCHEDULER', 'False') == 'True'

PERFORM_USER_HARVEST_EMAILS = env.get('SFM_PERFORM_USER_HARVEST_EMAILS', 'True') == 'True'
USER_HARVEST_EMAILS_HOUR = env.get('SFM_USER_HARVEST_EMAILS_HOUR', '1')
USER_HARVEST_EMAILS_MINUTE = env.get('SFM_USER_HARVEST_EMAILS_MINUTE', '0')

# Whether to scan the amount of free space on /sfm-data and /sfm-processing
PERFORM_SCAN_FREE_SPACE = env.get('SFM_PERFORM_SCAN_FREE_SPACE', 'True') == 'True'
SCAN_FREE_SPACE_HOUR_INTERVAL = env.get('SFM_SCAN_FREE_SPACE_HOUR_INTERVAL', '12')
# sfm data space threshold to send notification email,only ends with MB,GB,TB. eg. 500MB,10GB,1TB
DATA_THRESHOLD = env.get('DATA_VOLUME_THRESHOLD', '10GB')
# sfm processing space threshold to send notification email,only ends with MB,GB,TB. eg. 500MB,10GB,1TB
PROCESSING_THRESHOLD = env.get('PROCESSING_VOLUME_THRESHOLD', '10GB')

# Whether to scan the amount of free space on /sfm-data and /sfm-processing
PERFORM_MONITOR_QUEUE = env.get('SFM_PERFORM_MONITOR_QUEUE', 'True') == 'True'
# frequency to check the queue message length,default is 2 hour
MONITOR_QUEUE_HOUR_INTERVAL = env.get('SFM_MONITOR_QUEUE_HOUR_INTERVAL', '12')
# queue threshold for each harvester to send warning message
QUEUE_LENGTH_THRESHOLD = {
    'Sfm Ui': env.get('UI_QUEUE_LENGTH_THRESHOLD', '20'),
    'Twitter Rest Harvester': env.get('TWITTER_REST_HARVESTER_QUEUE_LENGTH_THRESHOLD', '5'),
    'Twitter Rest Harvester Priority': env.get('TWITTER_REST_HARVESTER_QUEUE_LENGTH_THRESHOLD', '5')
    # 'Flickr Harvester': '20',
    # 'Tumblr Harvester': '30',
    # 'Weibo Harvester': '30',
    # 'Weibo Exporter': '40',
    # 'Twitter Stream Exporter': '10',
    # 'Tumblr Exporter': '60',
    # 'Flickr Exporter': '70',
}
# other harvester not setting in above map, the default value will be 10
QUEUE_LENGTH_THRESHOLD_OTHER = env.get('QUEUE_LENGTH_THRESHOLD_OTHER', '5')

# Temporarily disabling scheduled serialization due to https://github.com/gwu-libraries/sfm-ui/issues/532.
PERFORM_SERIALIZE = env.get('SFM_PERFORM_SERIALIZE', 'True') == 'True'
SERIALIZE_HOUR = env.get('SFM_SERIALIZE_HOUR', '3')
SERIALIZE_MINUTE = env.get('SFM_SERIALIZE_MINUTE', '0')

SFM_UI_VERSION = "2.0.2"

# If a collection is schedules for <= PRIORITY_SCHEDULE_MINUTES,
# the routing key will have .priority appended.
PRIORITY_SCHEDULE_MINUTES = 60
# Harvest types that support priority queues.
PRIORITY_HARVEST_TYPES = ['twitter_search', 'twitter_user_timeline']