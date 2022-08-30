release: ./manage.py migrate && ./manage.py loaddata english.yaml && ./manage.py loaddata countries
web: gunicorn project.wsgi
