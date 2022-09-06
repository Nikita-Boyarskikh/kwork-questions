release: ./manage.py migrate && ./manage.py loaddata english.yaml && ./manage.py loaddata countries
web: gunicorn project.wsgi
worker: celery --app=project worker -l info
beat: celery --app=project beat -l info
