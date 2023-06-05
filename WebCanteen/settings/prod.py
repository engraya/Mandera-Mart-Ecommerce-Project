import django_on_heroku
from decouple import config


from .base import *


SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [
    'manderamartapp.herokuapp.com',
    'mandera.site'
]

#heroku settings
django_on_heroku.settings(locals(), staticfiles=False)
del DATABASES['default']['OPTIONS']['sslmode']

DEBUG_PROPAGATE_EXCEPTIONS = True

LOADING = {
        'version' : 1,
    'disable_exixting_loggers' : False,
    'formatters' :{
        'verbose' : {
        'format' : "[%a(asctime)s] %(leveltime)s [%(name)s : %(lineno)s] %(message)s",
        'datefmt' : "%d/%b/%Y %H:%M:%S"
    },
    'simple' : {
        'format' : '%(levelname)s %(message)s'
    },
},
'handlers' : {
    'console' : {
        'level' : 'DEBUG',
        'class' : 'logging-Streamhandler',
    },
},
'loggers' : {
    'MYAPP' : {
        'handlers' : ['console'],
        'level' : 'DEBUG',
    },
 }
}

