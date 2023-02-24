from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from models import Dapp
from . import db

dapp = Blueprint('dapp', __name__)
@dapp.route('/add-dapp', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def add_dapp():
    data = request.json
    # --- add to dapp table ---
    name = data["name"]
    dapp = Dapp.query.filter_by(name=name).first()
    if dapp:
        return jsonify({"message": "Dapp already exists"}), 409

    new_dapp = Dapp( dappAddress=data['address'],
        name=data['name'],
        url = data['url'],
        description = data['description'],
        image = data['image']
    )
    db.session.add(new_dapp)
    db.session.commit()
    return {"message":"dapp added"}, 200


@dapp.route('/get-dapps', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_dapps():
    dapps = Dapp.query.all()
    return jsonify(dapps), 200