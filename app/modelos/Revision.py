from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, SmallInteger, String, Table, Time, ForeignKey, func
from flask_sqlalchemy import SQLAlchemy
from flask import json

db = SQLAlchemy()
from app.helpers.utilidades import Utilidades

class Revision(db.Model):
    __tablename__ = 'revision'
    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, index=True, nullable=False)
    aprobado = db.Column(db.Integer, nullable=True)
    observaciones = db.Column(db.String(200), unique=False, nullable=False)
    fecha_revision = db.Column(db.Date)
    persona_id = db.Column(db.Integer, index=True, nullable=False)
    
    def __repr__(self):
        return '<Revision %r>' % self.id
    
    @classmethod
    def get_data_by_patente(cls, _patente):
        db.session.remove()
        from app.modelos.Vehiculo import Vehiculo
        
        query = db.session.query(Revision.id, Revision.observaciones, func.date_format(Revision.fecha_revision,'%d-%m-%Y').label('fecha_revision'), Revision.vehiculo_id, Vehiculo.patente).\
                select_from(Revision).\
                join(Vehiculo, Revision.vehiculo_id == Vehiculo.id).\
                filter(Vehiculo.patente == _patente).all()
        data = []

        if query:
            for r in query:
                data.append(
                    {
                        'id': r.id,
                        'fecha_revision': r.fecha_revision,
                        'observaciones': r.observaciones,
                        'vehiculo_id': r.vehiculo_id,
                        'patente': r.patente
                    }
                )
        return  data 

    @classmethod
    def insert_data(cls, dataJson):
        query = Revision( 
            id = None,
            vehiculo_id = dataJson['vehiculo_id'],
            #aprobado = Null,
            observaciones = dataJson['observaciones'],
            fecha_revision = dataJson['fecha_revision'],
            persona_id = dataJson['persona_id'],
            )
        Revision.guardar(query)
        if query.id:                            
            return  {'response': {'data': {'last_id': query.id} }} 
        return  None
    
    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            Revision.eliminar(query)
            if query.id:                            
                return query.id
        return  None

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()