"""
Django settings for alrowad_edu project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)5vwr1*1d80u83x2_ner0%%@t7x0rkrj75-0eup8oky*x_-d6f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
'countries',
    'academic',
    'admission',

    'attendance',
    'book_uniform',
    'calender',
    'clinic',
    'exams',
    "finance",
    'general_settings',
    'hr',
    'hostel',
    'library',
    'inventory',
    'reports',
    'social',
    'surveys',
    'timetable',
    'transport',
    'usermgr',
'student',



]

MIDDLEWARE = [
     'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'ratelimit.middleware.RatelimitMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'django_apscheduler.jobstores.DjangoJobStoreMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'usermgr.defenseMiddleware.DefenseMiddleware',
]

ROOT_URLCONF = 'alrowad_edu.urls'

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication', # if it active it required csrf
        'rest_framework.authentication.TokenAuthentication',  # <-- And here
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # active this only to protect
        # 'rest_framework.renderers.BrowsableAPIRenderer',

    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

# CORS_ORIGIN_WHITELIST = [
#     'http://192.168.11.111', 'http://192.168.11.24',
#     'http://192.168.11.80',
# ]
#
# CORS_ALLOWED_ORIGINS = ['http://192.168.11.32:3000',
#                         'http://192.168.11.31:3000', 'http://192.168.1.32',
#                         'http://192.168.11.111', 'http://192.168.11.24',
#                         'http://192.168.11.80:5173', 'http://192.168.11.80',
#                         ]

# CSRF_TRUSTED_ORIGINS = [
#     "http://192.168.11.111", "http://192.168.11.24",
#     'http://192.168.11.80',
# ]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    'x-encrypted-data',
]




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        # 'DIRS': [BASE_DIR / 'build'],
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

WSGI_APPLICATION = 'alrowad_edu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASE_ROUTERS = ['countries.router.DemoRouter','general_settings.router.DemoRouter1',
                    'student.router.StudentRouter','academic.router.AcademicRouter','usermgr.router.UserRouter']
DATABASE_APPS_MAPPING = {'alrowadedu_countries': 'alrowadedu_countries','default': 'alrowadedu_eman'}

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'alrowadedu_eman',
                'USER': 'postgres',
                'PASSWORD': '123',
                'HOST': 'localhost',
                'PORT': '5432',
    },
    'alrowadedu_countries': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'alrowadedu_countries',
                'USER': 'postgres',
                'PASSWORD': '123',
                'HOST': 'localhost',
                'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_DIRS = [
    BASE_DIR / 'src',
    BASE_DIR / 'public'
]
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_DIR = BASE_DIR / 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_HOST = 'smtp.titan.email'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'contact@alrowadit.com'
EMAIL_HOST_PASSWORD = 'AlR0w@d22AiT5P'
