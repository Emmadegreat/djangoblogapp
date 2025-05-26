import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from django.contrib.messages import constants as messages
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#STATIC_DIR = os.path.join(BASE_DIR, 'static')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'gistblog.up.railway.app',
    'gistblog.emftech.com.ng',
    'www.gistblog.emftech.com.ng'
]

CSRF_TRUSTED_ORIGINS = [
    'https://gistblog.up.railway.app',
    'https://gistblog.emftech.com.ng',
    'https://www.gistblog.emftech.com.ng'
]
PORT = os.getenv('PORT', '8000')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogapp',
    'dashboard',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 2

#django allauth config
# ACCOUNT_EMAIL_VERIFICATION = 'optional'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_UNIQUE_EMAIL = True
# SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD  = 'email'

# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
# SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_LOGIN_ON_GET = True


NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'blogapp.BlogUser'
ROOT_URLCONF = 'blogproject.urls'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blogapp.context_processors.get_categories',
            ],
        },
    },
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online',},
        'OAUTH_PKCE_ENABLED':True,
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = '/'

SESSION_COOKIE_AGE = 1209600 #two weeks
SESSION_COOKIE_SECURE = True
WSGI_APPLICATION = 'blogproject.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE'),
        'NAME': os.environ.get('DATABASE_NAME'),
        "PASSWORD": os.environ.get('DATABASE_PASSWORD'),
        "USER": os.environ.get('DATABASE_USER'),
        "HOST": os.environ.get('DATABASE_HOST'),
        "PORT": os.environ.get('DATABASE_PORT'),
    }
}

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'postgres',
        'PASSWORD': 'emf0046',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# POSTGRES_LOCALLY = True
# if ENVIRONMENT == 'production' or POSTGRES_LOCALLY == True:
#     DATABASES['default'] = dj_database_url.parse(env('DATABASE_URL'))



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

MESSAGE_TAGS = {
    messages.ERROR : 'danger'
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE_DIRS = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#password reset email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

#Default email addresses
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

#media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#cloudinary configuration

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)
