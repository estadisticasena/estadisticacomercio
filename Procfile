web: python manage.py migrate && python manage.py collectstatic --noinput && python create_superuser.py  && gunicorn analitica.wsgi:application --bind 0.0.0.0:$PORT
