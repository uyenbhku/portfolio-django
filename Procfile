web: gunicorn myapp.wsgi 
worker: python manage.py rqworker --job-class django_tasks_rq.Job