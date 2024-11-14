from sqlalchemy import CheckConstraint, Time, event
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import time

from ..db import db

class Actividad(db.Model):
    __tablename__ = 'actividades'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    hora_inicio = db.Column(Time, nullable=False)
    hora_fin = db.Column(Time, nullable=False)
    año_minimo = db.Column(db.Integer, nullable=False)
    año_maximo = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('hora_fin > hora_inicio', name='check_hora_fin_mayor_hora_inicio'),
        CheckConstraint('año_maximo > año_minimo', name='check_año_maximo_mayor_año_minimo'),
        CheckConstraint('año_minimo > 0 AND año_maximo > 0', name='check_años_positivos'),
    )

    @validates('hora_inicio', 'hora_fin')
    def validate_horas(self, key, value):
        if not isinstance(value, time):
            raise ValueError(f"{key} must be a valid time object")
        return value

    @validates('año_minimo', 'año_maximo')
    def validate_años(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{key} must be a positive integer")
        return value

    @hybrid_property
    def is_valid(self):
        return (
            self.hora_fin > self.hora_inicio and
            self.año_maximo > self.año_minimo and
            self.año_minimo > 0 and
            self.año_maximo > 0
        )

    def validate(self):
        if not self.is_valid:
            raise ValueError("Actividad is not valid")

@event.listens_for(Actividad, 'before_insert')
@event.listens_for(Actividad, 'before_update')
def receive_before_insert_update(mapper, connection, target):
    target.validate()

