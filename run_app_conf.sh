docker build -t ask .
docker run -it --rm -e MYSQL_HOST=172.17.0.2 --name ask ask bash
