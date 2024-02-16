from .database import db
from datetime import datetime

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    reservations = db.relationship('Reservation', backref='client', lazy='dynamic')

class Chambre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(80), nullable=False, unique=True)
    type = db.Column(db.String(80), nullable=False)
    prix = db.Column(db.String(80), nullable=False)
    reservations = db.relationship('Reservation', backref='chambre', lazy='dynamic')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'))
    id_chambre = db.Column(db.Integer, db.ForeignKey('chambre.id'))
    date_arrivee = db.Column(db.DateTime, default=datetime.utcnow)
    date_depart = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(80), nullable=False, default="Confirme")