# POS challenge
  
Code base to answer coding challenge for parrot interview. The code acts as a POS
for a restaurant.  

## Report endpoint
The report endpoint uses query parameters to set start_date and end_date. Please call as follows:
```bash
{{baseUrl}}/report/?start_date=2025-02-14&end_date=2025-02-19
```
  
## Testing
Create a file called .env.dev in the root directory of the project and add the following test env variables:
```bash
DJANGO_SETTINGS_MODULE='parrot.settings_dev'
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```
Test the code by executing the docker containers in attached mode
```bash
docker-compose up --build
```
build flag is only required for firtst run. Run in attached mode to see pytest results.  
  
Alternatively you can run locally by exporting the settings module environment variable and executing the test server.
```bash
python3 -m venv parrot
source parrot/bin/activate
python3 -m pip install -r requirements.dev.txt
export DJANGO_SETTINGS_MODULE='parrot.settings_local'
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
  
You may upload schema.yml to an API client to get up and running.

## Usage
The auth system works around a JWT bearer token. First generate the token and then add that to subsequent requests.

## Deploy to production
This application is configured to run in production in Heroku. Install the Heroku CLI and authenticate.  
Create the Heroku project and change the name to something more unique:
```bash
heroku create pos-challenge
```
Set the SECRETE_KEY:
```bash
heroku config:set SECRET_KEY='[YOUR_SECRET_KEY]'
```
Push to remote heroku git:
```bash
git push heroku master
```
Heroku creates a free database which is not suitable for production but will do for the purposes of the challenge. Run migrations for that database:
```bash
heroku run python manage.py migrate
```
