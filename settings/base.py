# Python imports
import os
from datetime import timedelta


# Organisation
ORGANISATION_NAME = 'Zürcher Studierendenzeitung'
ORGANISATION_REPLY_TO_EMAIL = 'support@zs-online.ch'
ORGANISATION_FROM_EMAIL = 'server@zs-online.ch'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = [
    'authentication.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'payment.apps.PaymentConfig',
    'subscription.apps.SubscriptionConfig',
    'user.apps.UserConfig',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'tags': 'utils.tags',
            },
        },
    },
]

# Specifies custom user model
AUTH_USER_MODEL = 'user.User'
# Authentication backends
AUTHENTICATION_BACKENDS = [
    'authentication.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Maximum amount of tokens per user
TOKENS_PER_USER = 2
# Validity duration of a token
TOKEN_EXPIRATION = timedelta(minutes=10)

# Password validation
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

# Fixed auth urls
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/auth/home/'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
