web: python manage.py migrate && python manage.py collectstatic --noinput && ./create_superuser.sh && gunicorn analitica.wsgi:application --bind 0.0.0.0:$PORT
