import environ
import os
from pathlib import Path
import django_heroku

print('Prod Mode')

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALLOWED_HOSTS = ['https://tasks-1.herokuapp.com/','localhost']

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('PROD_DB_NAME'),
        'USER': env('PROD_DB_USER'),
        'HOST': env('PROD_DB_HOST'),
        'PORT': env('PROD_DB_PORT')
    }
}

django_heroku.settings(locals())