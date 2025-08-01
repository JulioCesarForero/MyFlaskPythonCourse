import os
import secrets
from dotenv import load_dotenv

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager


from db import db

import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint 

# Cargar variables de entorno desde el archivo .env
load_dotenv() 



def create_app(db_url=None):
    
    app = Flask(__name__)
    
    # Environment-based configuration
    flask_env = os.getenv('FLASK_ENV', 'development')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.config['SQLALCHEMY_ECHO'] = flask_env == 'development'
    
    app.config["API_TITLE"] = os.getenv("API_TITLE", "Stores REST API")
    app.config["API_VERSION"] = os.getenv("API_VERSION", "v1")
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)


    # Set up JWT Manager - Usando variable de entorno del archivo .env
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if not jwt_secret:
        raise ValueError("JWT_SECRET_KEY no está configurado en el archivo .env")
    app.config["JWT_SECRET_KEY"] = jwt_secret

    jwt = JWTManager(app)
    
    # Configurar callbacks de JWT
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        """Define qué identificador usar en el token JWT"""
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Cargar usuario desde el token JWT"""
        from models.user import UserModel
        identity = jwt_data["sub"]
        return UserModel.query.filter_by(id=identity).one_or_none()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Callback para tokens expirados"""
        return {"message": "The token has expired.", "error": "token_expired"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Callback para tokens inválidos"""
        return {"message": "Signature verification failed.", "error": "invalid_token"}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Callback para tokens faltantes"""
        return {"message": "Request does not contain an access token.", "error": "authorization_required"}, 401

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)


    return app
