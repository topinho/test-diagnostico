from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, SmallInteger, String, Table, Time, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask import json

db = SQLAlchemy()
from app.helpers.utilidades import Utilidades

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(80), unique=False, nullable=False)
    modelo = db.Column(db.String(80), unique=False, nullable=False)
    patente = db.Column(db.String(20), unique=True, nullable=False)
    anio = db.Column(db.Integer)
    persona_id = db.Column(db.Integer, index=True, nullable=False)
    

    def __repr__(self):
        return '<Vehiculo %r>' % self.id

    @classmethod
    def get_data_by_patente(cls, _patente):
        db.session.remove()
        query =  cls.query.filter_by(patente =_patente).first()
        if query:
            return Utilidades.obtener_datos(query)
        else:
            return None
    
    @classmethod
    def insert_data(cls, dataJson):
        #return dataJson
        query = Vehiculo( 
            id = None,
            marca = dataJson['marca'],
            modelo = dataJson['modelo'],
            patente = dataJson['patente'],
            anio = dataJson['anio'],
            persona_id = dataJson['persona_id'],
        )
        Vehiculo.guardar(query)
        if query.id:                            
            return  {'response': {'data': {'last_id': query.id} }} 
        return  None
    
    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            Vehiculo.eliminar(query)
            if query.id:                            
                return query.id
        return  None

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()