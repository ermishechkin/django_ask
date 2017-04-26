docker build -t ask .
docker run -d -e MYSQL_HOST=172.17.0.2 --name ask ask python manage.py runserver 0.0.0.0:80
