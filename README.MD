# Installations
> download python 
- [python 3.6 +](https://python.org)
- browse how to install python properly

## INSTALL POSTGRESS & REQUIREMENTS UBUNTU
>##### sudo apt-get update
>##### sudo apt-get install python3-pip python-dev libpq-dev virtualenv
>##### sudo apt-get install wget ca-certificates
>##### sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
>##### sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
>##### sudo apt-get update
>##### sudo apt-get install postgresql postgresql-contrib
## INSTALL POSTGRESS & REQUIREMENTS WINDOWS
### install postgress
[tutorial](https://www.postgresqltutorial.com/install-postgresql/)
### Download Python 3.6+ 
[link](https://www.python.org/downloads/)

# CREATE DATABASE UBUNTU & WINDOWS
##### Create a Database and Database User
By default, Postgres uses an authentication scheme called “peer authentication” for local connections. Basically, this means that if the user’s operating system username matches a valid Postgres username, that user can login with no further authentication.

During the Postgres installation, an operating system user named postgres was created to correspond to the postgres PostgreSQL administrative user. We need to change to this user to perform administrative tasks:
## For Ubuntu
>#### ```sudo su - postgres```
You should now be in a shell session for the postgres user. Log into a Postgres session by typing:
## For Windows
[![N|Solid](https://sp.postgresqltutorial.com/wp-content/uploads/2019/05/Install-PostgreSQL-psql.png)](https://www.postgresqltutorial.com/install-postgresql/)
## RUN THE FOLLOWING COMMAND :
>#### ```psql```
First, we will create a database for our Django project. Each project should have its own isolated database for security reasons. We will call our database myproject in this guide, but it’s always better to select something more descriptive:

>#### ```CREATE DATABASE myproject;```
Remember to end all commands at an SQL prompt with a semicolon.

Next, we will create a database user which we will use to connect to and interact with the database. Set the password to something strong and secure:

>#### ```CREATE USER myprojectuser WITH PASSWORD 'password';```
Afterwards, we’ll modify a few of the connection parameters for the user we just created. This will speed up database operations so that the correct values do not have to be queried and set each time a connection is established.

We are setting the default encoding to UTF-8, which Django expects. We are also setting the default transaction isolation scheme to “read committed”, which blocks reads from uncommitted transactions. Lastly, we are setting the timezone. By default, our Django projects will be set to use UTC:

>#### ```ALTER ROLE myprojectuser SET client_encoding TO 'utf8';```
>#### ```ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';```
>#### ```ALTER ROLE myprojectuser SET timezone TO 'UTC';```
Now, all we need to do is give our database user access rights to the database we created:

>#### ```GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;```
Exit the SQL prompt to get back to the postgres user’s shell session:

>#### ```\q```
Exit out of the postgres user’s shell session to get back to your regular user’s shell session:

>#### ```exit```

# PREPARING SETUP TO RUN
>## WINDOWS
### check if python installed properly
```sh
python -V
```
### it should be print
```sh 
Python 3.7.5
```
### make virtualenv
```sh 
pip install virtualenv
```
```sh 
virtualenv env
```
### activate virtualenv
```sh 
env\scripts\activate
```
### should be look like this
```sh 
(env) pc-user:
```
>## UBUNTU
- if your os have installed python 3.7 you can change the version
```sh 
virtualenv env -p python3.6
```
### activate virtualenv
```sh 
source env/bin/activate
```
### should be look like this
```
(env) pc-user:
```

>## clone repo
```sh 
https://github.com/ribonred/django-frame.git
```
```sh 
cd django-frame
```
### make .env file inside backend folder, or you can edit on example.env file inside repo
```python
SECRET_KEY = ''
DEBUG = True
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# set true if u want use postgres, default is false using sqlite3
POSTGRES = False
#configurations postgres
#POSTGRES
DBNAME="your name database"
DBUSER="your name database user"
DBPASSWORD="your name database password"
DBHOST="localhost"
DBPORT=5432 
```
>## INSTALL REQUIREMENTS APPS
```sh 
pip install -r requirements.txt
```
>## how to get django secret key
```sh 
django-admin startproject yourprojectname
```
- navigate to yourproject folder/yourprojectnamefolder/settings.py
- copy secret key to .env file and delete all yourproject folder
## migrate and create superuser
```sh
python manage.py migrate
python manage.py createsuperuser
```
## running the server
### django server
```
python manage.py runserver
```
- navigate to 127.0.0.1:8000/admin to open django admin
### Create apps
```
django-admin startapp yourappname backendmodel
```
- navigate to .app to add your app model
- example
```sh
ADDITIONAL_APPS = backendmodel.yourappname1, backendmodel.yourappname2
```
you can install react vue or frontend framework on frontend folder