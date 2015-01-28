# encoding=utf-8

SECRET_KEY = 'tl$3pcr1^#!yg=1b7-%sff)xw#swi)z_2x&$5#a)$y8czhvjsz'
from tvenc.settings import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ENCODED_DIR = "/var/tv/encoded"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

LOGIN_URL = "/admin/login/"
STATIC_URL = '/static/'
