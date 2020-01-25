import os
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = [
    'compressor',
    'constance',
    'constance.backends.database',
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'post_office',
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
                'navigation': 'subscription_manager.utils.templatetags.navigation',
                'humanize': 'subscription_manager.utils.templatetags.humanize'
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

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'

TIME_ZONE = 'Europe/Zurich'
USE_I18N = False
USE_L10N = False

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
ADMINS = [('ZS Informatik', 'informatik@medienverein.ch')]
SERVER_EMAIL = 'server@zs-online.ch'

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
COMPRESS_ROOT = 'static_files/'

LIBSASS_OUTPUT_STYLE = 'compressed'
LIBSASS_SOURCEMAPS = True

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'TOKENS_PER_USER_PER_HOUR': (10, 'Maximale Anzahl gültiger Tokens pro Nutzerin', int),
    'TOKEN_EXPIRATION': (timezone.timedelta(days=3), 'Gültigkeitsdauer eines Tokens', timezone.timedelta),
    'EMAIL_ACCOUNTING': ('verlag@medienverein.ch', 'Rechnungen werden als Kopie an diese E-Mail-Adressen geschickt. E-Mail-Adressen müssen mit einem Semikolon getrennt sein.', str),
    'PERIOD_OF_PAYMENT': (timezone.timedelta(days=30), 'Rechnungen sind zahlbar innert', timezone.timedelta),
}
