"""
Django settings for sociofy project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3z4(7+@^^+pvba*+6@&&x3b2m!3awpwdmxd1*_kk_x&msx-0lh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sslserver',

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',

    'social_django',
]


EXTERNAL_APPS=['instagram','facebook','dashboard']

INSTALLED_APPS+=EXTERNAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'allauth.account.middleware.AccountMiddleware',
    # 'sslserver.middleware.SSLRedirectMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <-- Here
]

ROOT_URLCONF = 'sociofy.urls'

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL='/media/'

TEMPLATES = [
    
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                        os.path.join(BASE_DIR, 'shared_templates'),
                        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect', # <-- Here
             
            ],
        },
    },
]

WSGI_APPLICATION = 'sociofy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# social login facebook ----------------------------------------------------

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)




# Use SSL/TLS settings
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# # SSL Server settings
# SSLSERVER_CRT = '/home/kunal/Desktop/Projects/SocioFy-project/localhost.crt'  # Replace with the path to your certificate file
# SSLSERVER_KEY = '/home/kunal/Desktop/Projects/SocioFy-project/localhost.key'  # Replace with the path to your private key file




LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/accounts/'

SOCIAL_AUTH_FACEBOOK_KEY = '1392141388101711'  
SOCIAL_AUTH_FACEBOOK_SECRET = 'bf1260d487a10744bf2aa02eb24326c5' 



SOCIAL_AUTH_PIPELINE = (
    # 'social_core.pipeline.social_auth.social_details',
    # 'social_core.pipeline.social_auth.social_uid',
    # 'social_core.pipeline.social_auth.social_user',
    # 'social_core.pipeline.user.get_username',
    # 'social_core.pipeline.social_auth.associate_by_email',
    # 'social_core.pipeline.user.create_user',
    # 'social_core.pipeline.social_auth.associate_user',
    # 'social_core.pipeline.social_auth.load_extra_data',
    # 'social_core.pipeline.user.user_details',
    'dashboard.pipeline.save_access_token',
    'dashboard.pipeline.custom_redirect',

)



SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'read_insights',
    'pages_manage_cta',
    'pages_show_list',
    'business_management',
    'pages_messaging',
    'pages_messaging_subscriptions',
    'instagram_basic',
    'instagram_manage_comments',
    'instagram_manage_insights',
    'instagram_content_publish',
    'instagram_manage_messages',
    'page_events',
    'pages_read_engagement',
    'pages_manage_metadata',
    'pages_read_user_content',
    'pages_manage_posts',
    'instagram_manage_events'
]