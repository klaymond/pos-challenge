# POS challenge
  
Code base to answer coding challenge for parrot interview. The code acts as a POS
for a restaurant.  
  
## Testing
Test the code by executing the docker containers in attached mode
```bash
docker-compose up --build
```
build flag is only required for firtst run. Run in attached mode to see pytest results.  
  
Alternatively you can run locally by exporting the settings module environment variable and executing the test server.
```bash
export DJANGO_SETTINGS_MODULE='parrot.settings_local'
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
  
You may upload schema.yml to an API client to get up and running.

## Usage
The auth system works around a JWT bearer token. First generate the token and then add that to subsequent requests.