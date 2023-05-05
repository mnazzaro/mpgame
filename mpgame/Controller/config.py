SERVICE_TYPE_FOR_AUTH = 'GAME'

SECRET_KEY = 'super_secret_key'
JWT_SECRET = 'other_super_secret'

CELERY_RESULT_BACKEND = 'redis://host.docker.internal:6379'
CELERY_BROKER_URL = 'redis://host.docker.internal:6379'

REDIS_URI = 'redis://host.docker.internal:6379'
REDIS_HOST = 'redis://host.docker.internal:6379'

SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@host.docker.internal/mpdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False

CREATE_DB = True