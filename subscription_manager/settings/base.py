import os

import environ

from django.utils import timezone

# Define environment
env = environ.Env(
    SECRET_KEY=(str, ''),

    DATABASE_HOST=(str, 'localhost'),
    DATABASE_PORT=(int, 5432),
    DATABASE_NAME=(str, ''),
    DATABASE_USER=(str, ''),
    DATABASE_PASSWORD=(str, ''),

    EMAIL_HOST=(str, 'localhost'),
    EMAIL_PORT=(int, 587),
    EMAIL_HOST_USER=(int, ''),
    EMAIL_HOST_PASSWORD=(int, ''),
    EMAIL_USE_SSL=(bool, True)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# reading .env file
environ.Env.read_env(os.path.join(os.path.dirname(BASE_DIR), '.env'))

INSTALLED_APPS = [
    'compressor',
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cron',
    'import_export',
    'subscription_manager.administration.apps.AdministrationConfig',
    'subscription_manager.payment.apps.PaymentConfig',
    'subscription_manager.subscription.apps.SubscriptionConfig',
    'subscription_manager.user.apps.UserConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'subscription_manager.urls'

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
                'django.contrib.messages.context_processors.messages'
            ],
            'libraries': {
                'humanize': 'subscription_manager.utils.templatetags.humanize',
                'navigation': 'subscription_manager.utils.templatetags.navigation',
                'url_arguments': 'subscription_manager.utils.templatetags.url_arguments'
            },
        },
    },
]

AUTH_USER_MODEL = 'user.User'
AUTHENTICATION_BACKENDS = [
    'subscription_manager.user.backends.TokenBackend',
    'django.contrib.auth.backends.ModelBackend'
]

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

LOGIN_URL = '/anmelden/'
LOGIN_REDIRECT_URL = ''

LANGUAGE_CODE = 'de-ch'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)
STATIC_ROOT = "static_files/"

EMAIL_SUBJECT_PREFIX = '[ZS] '
DEFAULT_FROM_EMAIL = 'Zürcher Studierendenzeitung <server@zs-online.ch>'
DEFAULT_REPLY_TO_EMAIL = 'abo@zs-online.ch'
SERVER_EMAIL = 'server@zs-online.ch'
ADMINS = [('ZS Informatik', 'informatik@medienverein.ch')]
ACCOUNTING_EMAIL = 'abo@zs-online.ch'

CRON_CLASSES = [
    'subscription_manager.cron.SendEmails',
    'subscription_manager.cron.CleanDatabase'
]

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
COMPRESS_ROOT = 'static_files/'
COMPRESS_OUTPUT_DIR = 'cache'

LIBSASS_OUTPUT_STYLE = 'compressed'
LIBSASS_SOURCEMAPS = True

TOKENS_PER_USER_PER_HOUR = 20
TOKEN_EXPIRATION = timezone.timedelta(days=1)
PERIOD_OF_PAYMENT = timezone.timedelta(days=30)
