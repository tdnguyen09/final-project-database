import os

from flask import Flask, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SECRET_KEY'] = 'unique_string'
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SESSION_PERMANENT'] = True 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SESSION_COOKIE_SECURE'] = True  # True if using HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None' 
app.config['SESSION_COOKIE_DOMAIN'] = '.onrender.com'
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'




app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

# if __name__ == "__main__":
#     app.run(host='localhost', port=5000)