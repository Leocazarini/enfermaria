import os
import logging
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = BASE_DIR / 'logs'


# Load environment variables
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Authentication apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Providers
    'allauth.socialaccount.providers.google',

    # Project apps
    'appointments.apps.AppointmentsConfig',
    'controller.apps.ControllerConfig',
    'patients.apps.PatientsConfig',
    'reports.apps.ReportsConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'setup.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

def create_log_dirs():
    app_dirs = {
        'patients': ['views', 'models'],
        'appointments': ['views', 'models'],
        'controller': ['crud', 'api_totvs'],
    }
    
    for app, modules in app_dirs.items():
        for module in modules:
            dir_path = LOGS_DIR / app
            if not dir_path.exists():
                os.makedirs(dir_path)

# Crie os diretórios antes de configurar o logging
create_log_dirs()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        # Handlers app patients
        'patients_views_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'patients' / 'views.log',
            'formatter': 'verbose',
        },
        'patients_models_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'patients' / 'models.log',
            'formatter': 'verbose',
        },
        # Handlers app appointments
        'appointments_views_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'appointments' / 'views.log',
            'formatter': 'verbose',
        },
        'appointments_models_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'appointments' / 'models.log',
            'formatter': 'verbose',
        },
        # Handlers app controller
        'controller_crud_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'controller' / 'crud.log',
            'formatter': 'verbose',
        },
        'controller_api_totvs_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'controller' / 'api_totvs.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Loggers app patients
        'patients.views': {
            'handlers': ['patients_views_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'patients.models': {
            'handlers': ['patients_models_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Loggers app appointments
        'appointments.views': {
            'handlers': ['appointments_views_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'appointments.models': {
            'handlers': ['appointments_models_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Loggers app controller
        'controller.crud': {
            'handlers': ['controller_crud_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'controller.api_totvs': {
            'handlers': ['controller_api_totvs_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}







AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',  
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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'images/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ]

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR /'images'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Allauth settings

ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_ONLY = True

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'accounts/logout'