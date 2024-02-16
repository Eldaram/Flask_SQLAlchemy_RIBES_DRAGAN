from flask import Blueprint, jsonify, request
from .models import Client, Chambre, Reservation
from .database import db
from datetime import datetime
main = Blueprint('main', __name__)

def response(sucess, object, error="Il y a eu une error"): 
    message = ("Operation sur " + object + " effectee avec succes." if sucess else error )
    return {
        "sucess": sucess,
        "message": message
    }

def inside(a, b, c):
    return a <= b and b <= c

def date_parse_input(date):
    return datetime.strptime(date, '%m-%d-%Y')

@main.route('/api/clients', methods=['POST'])
def clients_ajout():
    new_client = Client(
        nom=request.json['nom'],
        email=request.json['email'],
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify(response(True, "Client"))

@main.route('/api/clients', methods=['GET'])
def clients():
    clients = Client.query.all()
    json_clients = []
    for client in clients:
        json_clients.append(
            {
                "id": client.id,
                "nom": client.nom,
                "email": client.email,
            }
        )
    return jsonify(json_clients)

@main.route('/api/chambres', methods=['GET'])
def chambres():
    chambres = Chambre.query.all()
    json_chambres = []
    for chambre in chambres:
        json_chambres.append(
            {
                "id": chambre.id,
                "numero": chambre.numero,
                "type": chambre.type,
                "prix": chambre.prix,
            }
        )
    return jsonify(json_chambres)

@main.route('/api/chambres', methods=['POST'])
def ajout_chambres():
    new_chambre = Chambre(
        numero=request.json['numero'],
        type=request.json['type'],
        prix=request.json['prix']
    )

    db.session.add(new_chambre)
    db.session.commit()

    return jsonify(response(True, "Chambre"))

@main.route('/api/chambres/<int:id>', methods=['PUT'])
def update_chambres(id):
    chambre = Chambre.query.get_or_404(id)
    if request.json["numero"]:
        chambre.numero = request.json["numero"]
    if request.json["type"]:
        chambre.type = request.json["type"]
    if request.json["prix"]:
        chambre.prix = request.json["prix"]
    db.session.commit()

    return jsonify(response(True, "Chambre"))

@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def delete_chambres(id):
    chambre = Chambre.query.get_or_404(id)
    db.session.delete(chambre)
    db.session.commit()

    return jsonify(response(True, "Chambre"))

@main.route('/api/chambres/disponibles', methods=['GET'])
def chambres_disponibles():
    if (not request.json["date_arrivee"] or 
        not request.json["date_depart"]):
        return jsonify(response(False, "Chambre", "Mauvaise requête"))
    try:
        date_arrivee = date_parse_input(request.json["date_arrivee"])
        date_depart = date_parse_input(request.json["date_depart"])
        if date_depart < date_arrivee:
            raise NameError()
    except:
        return jsonify(response(False, "Reservation", "Dates non valides"))
    chambres = Chambre.query.all()
    json_chambres = []
    for chambre in chambres:
        valid_chambre = True
        reservations = Reservation.query.filter(Reservation.id_chambre == chambre.id)
        for reservation in reservations:
            reservation_arrivee = reservation.date_arrivee
            reservation_depart  = reservation.date_depart
            if inside(date_arrivee, reservation_arrivee, date_depart) or inside(date_arrivee, reservation_depart, date_depart):
                valid_chambre = False
        if valid_chambre:
            json_chambres.append(
                {
                    "id": chambre.id,
                    "numero": chambre.numero,
                    "type": chambre.type,
                    "prix": chambre.prix,
                }
            )
    return jsonify(json_chambres)

@main.route('/api/reservations', methods=['GET'])
def reservations():
    reservations = Reservation.query.all()
    json_reservation = []
    for reservation in reservations:
        json_reservation.append(
            {
                "id": reservation.id,
                "id_client": reservation.id_client,
                "id_chambre": reservation.id_chambre,
                "date_arrivee": reservation.date_arrivee,
                "date_depart": reservation.date_depart,
                "type": reservation.type,
            }
        )
    return jsonify(json_reservation)

@main.route('/api/reservations', methods=['POST'])
def ajout_reservation():
    if (not request.json["id_client"] or 
        not request.json["id_chambre"] or 
        not request.json["date_arrivee"] or 
        not request.json["date_depart"]):
        return jsonify(response(False, "Reservation", "Mauvaise requête"))
    if not Client.query.get(request.json['id_client']):
        return jsonify(response(False, "Reservation", "Client non valide"))
    if not Chambre.query.get(request.json["id_chambre"]):
        return jsonify(response(False, "Reservation", "Chambre non valide"))
    try:
        date_arrivee = date_parse_input(request.json["date_arrivee"])
        date_depart = date_parse_input(request.json["date_depart"])
        if date_depart < date_arrivee:
            raise NameError()
    except:
        return jsonify(response(False, "Reservation", "Dates non valides"))
    new_reservation = Reservation(
        id_client=request.json['id_client'],
        id_chambre=request.json['id_chambre'],
        date_arrivee=date_arrivee,
        date_depart=date_depart,
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify(response(True, "Reservation"))

@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def suuprime_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()

    return jsonify(response(True, "Reservation"))