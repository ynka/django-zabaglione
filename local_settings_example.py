DEBUG = True
LOCAL_DEV = True


DATABASES = {
        'default': {
            'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'zabaglione_db',                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            }
        }


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
HAYSTACK_XAPIAN_PATH = 'path-to-haystack-data-directory'

MERCURIAL_BIN = '/usr/local/bin/hg'
