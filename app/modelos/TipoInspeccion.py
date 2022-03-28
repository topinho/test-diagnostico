from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, SmallInteger, String, Table, Time
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TipoInspeccion(db.Model):
    __tablename__ = 'tipo_inspeccion'
    id = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return '<TipoInspeccion %r>' % self.id
