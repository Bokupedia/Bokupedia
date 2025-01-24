from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-97&w1m6fw*uww*sblgwv)as-+d!1tz@q-z^(5bx9xf0tv%8+oo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['Bokupedia.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'user_accounts',
    'discussion_forum',
    'private_messages',
    'post_interactions',
    'notifications',
    'django_ckeditor_5',
]      

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading',
            '|',
            'bold', 'italic', 'strikethrough', 'underline', 'code', 'subscript', 'superscript',
            '|',
            'bulletedList', 'numberedList',
            '|', 
            'outdent', 'indent',
            '|',
            'link', 'uploadImage', 'blockQuote', 'insertTable', 'mediaEmbed',
            '|',
            'undo', 'redo',
            '|',
            'alignment',
            '|',
            'fontFamily', 'fontSize', 'fontColor', 'fontBackgroundColor',
            '|',
            'findAndReplace', 'sourceEditing'
        ],
        'upload': True,
        'mediaEmbed': {
            'previewsInData': True, 
        }
    }
}

CSP_FRAME_SRC = ["https://www.youtube.com"]
CSP_DEFAULT_SRC = ["'self'", "https://www.youtube.com"]

CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

AUTH_USER_MODEL = 'user_accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CyberHex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE_DIR, 'CyberHex/templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'CyberHex.context_processors.unread_notifications',
                'CyberHex.context_processors.unread_messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CyberHex.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True 
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / "static"]


STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = 'static/'
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user_accounts.User'

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"
