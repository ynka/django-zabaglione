# -*- coding: utf-8 -*-

# Django settings for zabaglione project.
import os
import sys
from local_settings import *

TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)
sys.path.append(PROJECT_DIR)

ADMINS = (
        # ('Your Name', 'your_email@domain.com'),
        )

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR,'site_media')
LANGUAGE_CODE = 'pl'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!ta_t9e5&^e33ll1c=5)(#+lms&$p%2k!0=t_r!g+km=ihv)!w'

# This is the number of days users will have to activate their accounts after registering. If a user does not activate within that period, the account will remain permanently inactive and may be deleted by maintenance scripts provided in django-registration.
#
ACCOUNT_ACTIVATION_DAYS = 7

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'sphene.community.groupaware_templateloader.load_template_source',
        #     'django.template.loaders.eggs.Loader',
        )

MIDDLEWARE_CLASSES = [
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.contrib.csrf.middleware.CsrfMiddleware',
        'django_sorting.middleware.SortingMiddleware',
        'pagination.middleware.PaginationMiddleware',
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        'sphene.community.middleware.ThreadLocals',
        'sphene.community.middleware.GroupMiddleware',
        ]

LOGIN_REDIRECT_URL = '/'
ROOT_URLCONF = 'zabaglione.urls'

TEMPLATE_DIRS = (
        os.path.join(PROJECT_DIR,'templates')
        )

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.contrib.messages.context_processors.messages",
        "django.core.context_processors.request",
        "core.context_processors.add_flatpages",
        'django.core.context_processors.request',
        )

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'zabaglione.object_permissions.backends.ObjectPermBackend',
        )

INSTALLED_APPS = (
        # django contrib apps
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.flatpages',
        'django.contrib.admin',
        'django.contrib.comments',
        'django.contrib.markup',

        # third party apps
        'south',
        'django_nose', # MUSI byc po south
        'django_extensions',
        # 'registration',
        'django_sorting',
        'django_filters',
        'pagination',
        'haystack',
        'attachments',
#        'test_utils',

        # own apps
        'core',
        'object_permissions',
        )
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
AUTH_PROFILE_MODULE = 'TODO.TODO'
HAYSTACK_SITECONF = 'zabaglione.search_sites'
HAYSTACK_SEARCH_ENGINE = 'xapian'


