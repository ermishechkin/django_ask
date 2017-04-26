docker build -t ask .
docker run -p 80:80 -it --rm -e MYSQL_HOST=172.17.0.2 --name ask ask bash
