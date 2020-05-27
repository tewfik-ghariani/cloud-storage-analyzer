

Cloud Storage Analyzer project.

# Description

A web application providing features such as data aggregation, anomalies detection and data inspection of files residing in AWS S3 buckets
The tool leverages AWS Athena by using its JDBC driver

- Creation 
01 March 2017
- Author 
Tewfik Ghariani


# Configuration

Hi there!

Before starting to use the application, you have to set your environment.
Don't worry, you need to follow these steps and you'll be ready!

### Python 3

### JAVA 8

### Pip
```sh
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv
```



### Virtual Environment
```sh
$ virtualenv venv
```
Activate your virtual environment, (You can turn it off afterwards by typing simply deactivate)
```sh
$ source venv/bin/activate
```



### Postgres:

> PostgreSQL 9.4 version is mandatory since the application uses the JsonB object type.

```sh
$ sudo apt-get install postgresql-9.4
$ sudo su - postgres
$ psql
```

```sql
CREATE DATABASE athena_db;
CREATE USER si_aps WITH PASSWORD {% _<password>_ %} ;
ALTER ROLE si_aps SET client_encoding TO 'utf8';
ALTER ROLE si_aps SET default_transaction_isolation TO 'read committed';
ALTER ROLE si_aps SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE athena_db TO si_aps;
\q
```

```sh
$ exit
```



Ref :
[Django + Postgres][df1]



### Bower Configuration
```sh
$ sudo apt-get install npm
$ sudo  npm install -g bower
```

In case of error:
```sh
$ sudo ln -s /usr/bin/bower /usr/local/bin/bower
```

or

```sh
$ sudo ln -s /usr/bin/nodejs /usr/bin/node
```

### Python Dependencies

```sh
$ pip install -r requirements.txt
```

### Front-end Dependencies 

```sh
$ python manage.py bower install
```

### DataBase Migration

```sh
$ python manage.py makemigrations
$ python manage.py migrate
```


 ```$ python manage.py collectstatic (Only in prod)```


# Usage



### Admin account 
```sh
$ python manage.py createsuperuser
```

### Run the server!

```sh
$ python manage.py runserver
```


> http://127.0.0.1:8000/ 


Your environment is set up
Follow these instructions to use our prototype and contribute in the development process of our analyzer



[df1]: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
