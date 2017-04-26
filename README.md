# django_ask

### Step 0. [Docker installation (Debian)](https://docs.docker.com/engine/installation/)
```bash
sudo apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
```

### Step 1. Clone repository
```bash
git clone https://github.com/ermishechkin/django_ask.git
```

### Step 2. MySQL (machine 1)
```bash
sudo ./run_mysql.sh
```

### Step 3. Initial config django app (machine 2)
Change IP to MySQL machine IP in run_app_conf.sh, then run it:
```bash
sudo ./run_app_conf.sh

python manage.py makemigrations
python manage.py makemigrations ask
python manage.py migrate

python manage.py shell
```
```python
import ask.generate as g
g.gen_many()
[Ctrl-D]
[Ctrl-D]
```

### Step 4. Run django app on some machines (machines 2-4)
Change IP to MySQL machine IP in run_app.sh, then run it:
```bash
sudo ./run_app.sh
```

### Step 5. Haproxy (machine 5 or 1)
Chang IPs to machines's 2-4 IPs in run_haproxy.sh and run_it
```bash
sudo ./run_haproxy.sh
```
