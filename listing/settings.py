import os
import urlparse
# Django settings for listing project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
 
MANAGERS = ADMINS
USING_OPENSHIFT_DB=0
SERVER_URL= "http://127.0.0.1:8000/"
if 'OPENSHIFT_MYSQL_DB_URL' in os.environ:
    SERVER_URL= "http://rentlisting-snowleo.rhcloud.com/"	
    url = urlparse.urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))
    DATABASES = {
        'default': {	
			'ENGINE' : 'django.db.backends.mysql',
			'NAME': os.environ['OPENSHIFT_APP_NAME'],
			'USER': url.username,
			'PASSWORD': url.password,
			'HOST': url.hostname,
			'PORT': url.port,
        }
	}
elif USING_OPENSHIFT_DB : 
    SERVER_URL= "http://rentlisting-snowleo.rhcloud.com/"	
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rentlisting',
        'USER': 'adminSCiVVaW',
        'PASSWORD': 'xLVJRwPPpEfN',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3307',                      # Set to empty string for default.
    }
}	
else:
    SERVER_URL= "http://127.0.0.1:8000/"
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'listing_db',
        'USER': 'root',
        'PASSWORD': 'c8177818',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
    }
    }

install_requires=['Django>=1.5','MySQL-python','facebook-sdk','django-cors-headers'],  

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
CORS_ORIGIN_ALLOW_ALL =False
CORS_ALLOW_CREDENTIALS =True
# CORS_ORIGIN_WHITELIST = (
    # '127.0.0.1',
	# 'localhost:3000',
	# '.nightspirit.info'
# )
CORS_ORIGIN_REGEX_WHITELIST = (
    '(^http?://(\w+\.)?nightspirit\.info(:\d+)?$)',
    '(^http?://127.0.0.1(:\d+)?$)',
    )
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
if 'OPENSHIFT_DATA_DIR' in os.environ:
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')
else:
    MEDIA_ROOT = os.path.join('C:\Users\ChiYo Hsiao\Desktop\projects', "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
if 'OPENSHIFT_REPO_DIR' in os.environ:
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
else:
    STATIC_ROOT = os.path.join('C:\Users\ChiYo Hsiao\Desktop\projects\/rentlisting\wsgi', 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (

    "~/app-root/runtime/dependencies/python/virtenv/lib/python2.7/site-packages/django_facebook-5.3.1-py2.7.egg/django_facebook/static/",
    "/var/lib/openshift/535f15f24382ec097600087f/app-root/runtime/dependencies/python/virtenv/lib/python2.7/site-packages/django_facebook-5.3.1-py2.7.egg/django_facebook/static/",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7snsv^l97a=94=j^25m8*y^k^6l(a$5m1o8679a-2*e$qe9#89'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',		
)

ROOT_URLCONF = 'listing.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'listing.wsgi.application'

TEMPLATE_DIRS = (
    'templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'polls',
    'login',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook', 	
    'corsheaders',	
    'django_facebook',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_facebook.context_processors.facebook',
)
AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)
FACEBOOK_APP_ID='490262681101649'
FACEBOOK_APP_SECRET='575dac4016294acd3851cda734fddf21'
FACEBOOK_STORE_FRIENDS =True
# FACEBOOK_CELERY_STORE=True
AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'
AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1.0, 
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
MAX_PROFILE_PIC_SIZE= 2*1024*1024 
EMAIL_USE_TLS= True
EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER ="nestq2014@gmail.com"
EMAIL_HOST_PASSWORD="nestqqqq"
EMAIL_PORT = 587


# EMAIL_USE_SSL = True