from decimal import Decimal
from functools import partial
from pathlib import Path

from dj_database_url import parse as db_url
import moneyed
from decouple import config, Csv
from django.contrib import messages
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as __


def optional(cast):
    def optional_cast(value):
        if value is None:
            return value
        return cast(value)

    return optional_cast


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'project' / 'static',
]
MEDIA_ROOT = BASE_DIR / 'media'

SECRET_KEY = config('SECRET_KEY', default='django-insecure-kj4f#g8&3tlkrxu_$m=txxg(xh2e_f3wj7)qjj1+%tsv8gww05')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())
DEBUG = config('DEBUG', default=False, cast=bool)

INSTALLED_APPS = [
    # Admin
    'baton',
    'django.contrib.admin',

    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # 3rd party
    'anymail',
    'djmoney',
    'captcha',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'crispy_bootstrap5',
    'constance',
    'constance.backends.database',

    # Project
    'accounts',
    'answers',
    'chat',
    'claims',
    'countries',
    'languages',
    'likes',
    'questions',
    'users',
    'rules',

    'baton.autodiscover',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [BASE_DIR / 'templates'],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                'constance.context_processors.config',

                'project.context_processors.language',
                'project.context_processors.menu_items',
                'project.context_processors.countries',
            ],
            'builtins': ['project.templatetags.global'],
        },
    },
]

ROOT_URLCONF = 'project.urls'
AUTH_USER_MODEL = 'users.User'
WSGI_APPLICATION = 'project.wsgi.application'

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

db_url = partial(db_url, conn_max_age=600)
DATABASES = {
    'default': config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}', cast=db_url),
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

TIME_ZONE = config('TIME_ZONE', default='UTC')
USE_I18N = True
USE_L10N = False
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / 'locale']
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', __('English')),
]

FIXTURE_DIRS = [BASE_DIR / 'fixtures']

# Email
ANYMAIL = {
    'MAILGUN_API_KEY': config('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': config('MAILGUN_DOMAIN'),
    'DEBUG_API_REQUESTS': DEBUG,
    'SEND_DEFAULTS': {
        'track_clicks': True,
        'track_opens': True,
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'anymail.backends.mailgun.EmailBackend'
# EMAIL_HOST = config('MAILGUN_SMTP_SERVER')
# EMAIL_PORT = config('MAILGUN_SMTP_PORT')
# EMAIL_HOST_USER = config('MAILGUN_SMTP_LOGIN')
# EMAIL_HOST_PASSWORD = config('MAILGUN_SMTP_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = config('SERVER_EMAIL')

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.ERROR: 'danger',
}

# Logging

LOG_LEVEL = config('LOG_LEVEL', default='INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {'level': LOG_LEVEL, 'handlers': ['console']},
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True,
        },
    },
}

# Security

SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_HSTS_SECONDS = 0 if DEBUG else 24 * 60 * 60

# Celery

REDIS_URL = config('REDISCLOUD_URL', default=f'redis://localhost:6379')
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = DEBUG
CELERY_TASK_EAGER_PROPAGATES = DEBUG

# Cache

CACHES = {
    'default': {
        'BACKEND': (
            'django.core.cache.backends.locmem.LocMemCache'
            if DEBUG else
            'django.core.cache.backends.redis.RedisCache'
        ),
        'LOCATION': REDIS_URL,
    }
}

# Templates

CRISPY_ALLOWED_TEMPLATE_PACKS = 'crispy_forms'
CRISPY_TEMPLATE_PACK = 'crispy_forms'

# Admin

ADMINS = MANAGERS = [
    ('Nikita', 'N02@yandex.ru'),
]

SITE_ID = config('SITE_ID', default=1, cast=int)


def _get_current_site_name(*args, **kwargs):
    from django.contrib.sites.models import Site
    return Site.objects.get(id=SITE_ID).name


BATON = {
    'GRAVATAR_DEFAULT_IMAGE': 'mp',
    'SITE_HEADER': '<img src="/%s/logo.png" />' % STATIC_URL,
    'SITE_TITLE': lazy(_get_current_site_name),
    'INDEX_TITLE': __('Site administration'),
}

# Authentication

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'users:me'
ACCOUNT_LOGOUT_REDIRECT_URL = LOGOUT_REDIRECT_URL = 'index'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_FORMS = {
    'signup': 'users.forms.SignupForm',
}
ACCOUNT_ADAPTER = 'users.auth.AccountAdapter'
ACCOUNT_UNIQUE_EMAIL = False
# TODO: not secure
ACCOUNT_LOGOUT_ON_GET = True

# Currencies

USDT = moneyed.add_currency(code='USDT', numeric=None, name=__('USDT crypto currency'))

DEFAULT_CURRENCY = USDT.code
CURRENCIES = [DEFAULT_CURRENCY]
CURRENCY_CODE_MAX_LENGTH = 4

# Constance

CONSTANCE_CONFIG = {
    'DEFAULT_COUNTRY': ('united_states', __('Default user country'), str),
    'DEFAULT_LANGUAGE': ('en', __('Default language'), str),
    'MIN_QUESTION_PRICE': (Decimal(0), __('Minimal question price'), Decimal),
    'ANSWER_PREVIEW_TEXT_SIZE': (50, __('Answer preview text size'), int),
    'PUBLISH_QUESTION_COUNTDOWN_HOURS': (24, __('Publish question countdown hours'), int),
    'CLOSE_ANSWERS_COUNTDOWN_HOURS': (24, __('Close answers countdown hours'), int),
    'FINISH_VOTING_COUNTDOWN_HOURS': (24, __('Finish voting countdown hours'), int),
}

CONSTANCE_CONFIG_FIELDSETS = (
    (
        __('Defaults'),
        (
            'DEFAULT_COUNTRY',
            'DEFAULT_LANGUAGE',
        ),
    ),
    (
        __('Countdowns settings'),
        (
            'PUBLISH_QUESTION_COUNTDOWN_HOURS',
            'CLOSE_ANSWERS_COUNTDOWN_HOURS',
            'FINISH_VOTING_COUNTDOWN_HOURS',
        ),
    ),
    (
        __('Other settings'),
        (
            'MIN_QUESTION_PRICE',
            'ANSWER_PREVIEW_TEXT_SIZE',
        ),
    ),
)
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

# Custom

GOOGLE_APPLICATION_CREDENTIALS = config('GOOGLE_APPLICATION_CREDENTIALS')
