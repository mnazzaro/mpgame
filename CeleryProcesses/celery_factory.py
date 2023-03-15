from celery import Celery

def create_celery (app=None):
    if app:
        # This is the app instance
        celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], 
                        broker=app.config['CELERY_BROKER_URL'], include=['tasks'])
        celery.conf.update(app.config)
        class ContextTask (celery.Task):
            abstract = True
            def __call__ (self, *args, **kwargs):
                with app.app_context():
                    return celery.Task.__call__(self, *args, **kwargs)
        celery.Task = ContextTask
    else:
        celery = Celery(__name__)
        celery.config_from_object('celeryconfig')
    
    return celery
