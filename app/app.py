import redis
import os
import json
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from app.modelos import *

app = Flask(__name__)
api = Api(app)
cache = redis.Redis(host='redis', port=6379)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)
db.init_app(app)
# create the DB on demand
@app.before_first_request
def create_tables():
    db.create_all()

from app.recursos.Persona import Personas, PersonaSave
from app.recursos.Revision import Revisiones, RevisionSave, RevisionesPorPatente
from app.recursos.Inspeccion import Inspecciones, InspeccionSave, InspeccionDelete
"""
@app.route('/hello')
def hello():
    return 'Hello, World'
"""
api.add_resource(Personas, '/personas')
api.add_resource(PersonaSave, '/personas/save')

#api.add_resource(Revisiones, '/revisiones')
api.add_resource(RevisionSave, '/revisiones/save')
api.add_resource(RevisionesPorPatente, '/revisiones/por-patente/<patente>')

api.add_resource(Inspecciones, '/inspecciones')
api.add_resource(InspeccionSave, '/inspecciones/save')
api.add_resource(InspeccionDelete, '/inspecciones/delete/<id>')