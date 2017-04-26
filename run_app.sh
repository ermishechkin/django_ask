docker build -t ask .
docker run -d -p 80:80 -e MYSQL_HOST=172.17.0.2 --name ask ask
