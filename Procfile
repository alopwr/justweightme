release: python manage.py migrate
web: gunicorn slimmerme.wsgi --log-file -
worker: celery worker -A slimmerme -l info
