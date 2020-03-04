from django.core.management import call_command

from celery import app


@app.task
def clearsessions():
    call_command('clearsessions')
