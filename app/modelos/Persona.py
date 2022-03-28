from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, SmallInteger, String, Table, Time
from flask_sqlalchemy import SQLAlchemy
from flask import json

db = SQLAlchemy()
from app.helpers.utilidades import Utilidades

class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(80), unique=False, nullable=False)
    apellido = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Persona %r>' % self.id
    
    @classmethod
    def get_data_by_identificacion(cls, _id):
        db.session.remove()
        query =  cls.query.filter_by(identificacion=_id).first()
        if query:
            return Utilidades.obtener_datos(query)
        else:
            return None
    
    @classmethod
    def insert_data(cls, dataJson):
        #return dataJson
        query = Persona( 
            id = None,
            identificacion = dataJson['identificacion'],
            nombre = dataJson['nombre'],
            apellido = dataJson['apellido'],
            )
        Persona.guardar(query)
        if query.id:                            
            return  {'response': {'data': {'last_id': query.id} }} 
        return  None
    
    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            Persona.eliminar(query)
            if query.id:                            
                return query.id
        return  None

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()