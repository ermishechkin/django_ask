docker run -d -p 80:80 --name hap -v "$(pwd)/hap_etc:/usr/local/etc/haproxy:ro" haproxy:1.7
