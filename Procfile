release: ./manage.py migrate && ./manage.py loaddata languages && ./manage.py loaddata countries
web: gunicorn project.wsgi
worker: celery --app=project worker -B -l info
