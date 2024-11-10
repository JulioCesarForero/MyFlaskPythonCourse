# Notas del proyecto para tener en cuenta su correcta ejecucion 

## Activate Virtual Py Environment 

.venv\Scripts\activate

## Install requirements

pip install -r requirements.txt

pip install Flask

python.exe -m pip install --upgrade pip

## run app in local development environment

flask run

## build Docker image 

docker build -t rest-apis-flask-python .


docker run -p 5005:5000 rest-apis-flask-python


docker run -dp 5005:5000 rest-apis-flask-python


docker compose up


docker compose up --build --force-recreate --no-deps web


## forma de ejecutar mi aplicacion de Flask en Docker 

    docker build -t flask-smorest-api .


    docker run -dp 5005:5000 flask-smorest-api

## Creacion de un volumen en Docker 

### MAC
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api

### Windows
docker run -dp 5005:5000 -w /app -v "%cd%:/app" flask-smorest-api

docker run -dp 5005:5000 -w /app -v "C:\MISO\Tutoriales\flask:/app" flask-smorest-api


## al usar Flask Morris swagger-ui ya tenemos documentado nuestras apis

http://localhost:5005/swagger-ui


## opciones .flaskenv options 

FLASK_APP=app 
FLASK_DEBUG=1
 o 
FLASK_APP=app 
FLASK_ENV=development

