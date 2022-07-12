release: ./manage.py migrate && ./manage.py loaddata english.yaml
web: gunicorn project.wsgi
