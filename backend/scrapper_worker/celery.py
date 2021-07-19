from celery import Celery

app = Celery('scrapper_worker',
             include=['scrapper_worker.tasks'])

app.conf.broker_url = "redis://redis:6379/0"
app.conf.result_backend = "redis://redis:6379/0"
app.conf.timezone = 'UTC'