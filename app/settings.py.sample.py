IOS_APPS = {
    'consumer': {
        'id': 'dummy',
    },
    'provider': {
        'id': 'dummy'
    }
}

ANDROID_APPS = {
    'consumer': {
        'packageName': 'dummy package name',
        'credentials': {}
    },
    'provider': {
        'packageName': 'dummy package name',
        'credentials': {}
    }
}

CRM = {
    'freshdesk': {
        'domain': 'dummy',
        'api_key': 'dummy',
        'password': 'dummy'
    }
}

BACKEND = 'csv'

APP_NAME = 'app'

DEBUG = False
TESTING = False

# SQLAlchemy configs
DB_HOST = 'mysql'
DB_NAME = 'dummy'
DB_USER = 'root'
DB_PASS = ''
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
    DB_USER, DB_PASS, DB_HOST, DB_NAME
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
