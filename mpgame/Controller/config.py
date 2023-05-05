SERVICE_TYPE_FOR_AUTH = 'GAME'

SECRET_KEY = 'super_secret_key'
JWT_SECRET = 'other_super_secret'

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'

REDIS_URI = 'redis://127.0.0.1:6379'

SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@127.0.0.1/mpdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False

CREATE_DB = True