from celery import Celery

def create_celery (app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], 
                        broker=app.config['CELERY_BROKER_URL'], include=['tasks'])
    
    celery.conf.update(app.config)
    class ContextTask (celery.Task):
        abstract = True
        def __call__ (self, *args, **kwargs):
            with app.app_context():
                return celery.Task.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
