release: python manage.py migrate
release: python manage.py loaddata sports.json
release: python manage.py loaddata bookmakers.json
web: gunicorn sports_bet_site.wsgi