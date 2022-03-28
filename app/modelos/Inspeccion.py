from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, SmallInteger, String, Table, Time, ForeignKey
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Inspeccion(db.Model):
    __tablename__ = 'inspeccion'
    id = db.Column(db.Integer, primary_key=True)
    revision_id = db.Column(db.Integer, index=True)
    tipo_inspeccion_id = db.Column(db.Integer, index=True)
    observaciones = db.Column(db.String(200), unique=False, nullable=False)
    estado = db.Column(db.String(40))
    persona_id = db.Column(db.Integer, index=True, nullable=False)

    def __repr__(self):
        return '<Revision %r>' % self.id
    
    @classmethod
    def get_data_by_id(cls, _id):
        db.session.remove()
        query =  cls.query.filter_by(id=_id).first()
        return query

    @classmethod
    def insert_data(cls, dataJson):
        #return dataJson
        query = Inspeccion( 
            id = None,
            revision_id = dataJson['revision_id'],
            tipo_inspeccion_id = dataJson['tipo_inspeccion_id'],
            observaciones = dataJson['observaciones'],
            estado = dataJson['estado'],
            persona_id = dataJson['persona_id'],
        )
        Inspeccion.guardar(query)
        if query.id:                            
            return  {'response': {'data': {'last_id': query.id} }} 
        return  None
    
    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            Inspeccion.eliminar(query)
            if query.id:                            
                return query.id
        return  None

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()