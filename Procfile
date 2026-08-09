web: gunicorn myapp.wsgi --bind 0.0.0.0:$PORT
worker: python manage.py rqworker --job-class django_tasks_rq.Job