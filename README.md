



# Activate Virtual Py Environment 

.venv\Scripts\activate



pip install -r requirements.txt

pip install Flask

python.exe -m pip install --upgrade pip



flask run


docker build -t rest-apis-flask-python .


docker run -p 5005:5000 rest-apis-flask-python


docker run -dp 5005:5000 rest-apis-flask-python


docker compose up


docker compose up --build --force-recreate --no-deps web


### forma de ejecutar mi aplicacion de Flask en Docker 

    docker build -t flask-smorest-api .


    docker run -dp 5005:5000 flask-smorest-api

## Creacion de un volumen en Docker 
MAC
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api

Windows
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




# old app.py

from flask import   Flask, request
from db import items, stores

app = Flask(__name__)


stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

@app.get("/store")  #http://127.0.0.1:5000/store
def get_stores():
    return {"stores": stores}


@app.post("/store")  #http://127.0.0.1:5000/store
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
        
    return {"message": "Store not found"}, 404
    

@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
           return store, 201  
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
           return {"items": store["items"]}, 201  
    return {"message": "Store not found"}, 404


# Old Api 2

import uuid
from flask import   Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.get("/store")  #http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message = "Store not found.")


@app.post("/store")  #http://127.0.0.1:5000/store
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400, 
            message = "Bad request. Ensure 'name' is included in the JSON payload",
        )
        
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message= f"Store alredy exist.")
    
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")
        

# ITEMS

@app.get("/item") 
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message = "Item not found.")
        
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")
    
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    # There's  more validation to do here!
    # Like making sure price is a number, and also both items are optional
    # Difficult to do with an if statement...
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        )
    try:
        item = items[item_id]
        # https://blog.teclado.com/python-dictionary-merge-update-operators/
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")

@app.post("/item")
def create_item():
    item_data = request.get_json()
    
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message = "Bad request. ensure 'price', 'store_id', an 'name' are include in the JSON payload."
        )
        
    for item in items.values():
        if (
            item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]
        ):
            abort(404, message = f"Item already exist.")
    
    
    if item_data["store_id"] not in stores:
        abort(404, message = "Store not found.")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    
    return item, 201
