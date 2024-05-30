import os
import secrets

import django
from django.conf import global_settings

DB_NAME_PREFIX = 'test_mellon_'
DB_NAME = DB_NAME_PREFIX + secrets.token_hex(63)[: 63 - len(DB_NAME_PREFIX)]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'TEST': {
            'NAME': DB_NAME,
        },
    }
}
DEBUG = True
SECRET_KEY = 'xx'
STATIC_URL = '/static/'
INSTALLED_APPS = ('mellon', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions')
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mellon.middleware.PassiveAuthenticationMiddleware',
]

AUTHENTICATION_BACKENDS = ('mellon.backends.SAMLBackend',)
ROOT_URLCONF = 'urls_tests'
TEMPLATE_DIRS = [
    'tests/templates/',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': TEMPLATE_DIRS,
    },
]
