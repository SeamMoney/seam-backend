# general imports
from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify

# cors + authentication
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

# sql execution
from . import db
from .models import *
import sqlalchemy
import urllib.parse

import json

main = Blueprint('main', __name__)
# test
@main.route('/')
def index():
    return 200
    # return render_template('index.html')

@main.route('/spot_prices', methods=['GET'])
@cross_origin(origin='*')
def spot_prices():
    # get all oracles
    oracles = Oracle.query.limit(10).all()


    return {"data": oracles}, 200

@main.route('/profile')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def my_profile():
    current_user = get_jwt_identity()
    user_stashes = Stash.query.filter_by(userId=current_user).all()
    user_info = User.query.filter_by(userId=current_user).first()
    temp_user = user_info.get_user()
    temp_user['stashes'] = json.user_stashes
    print(temp_user)
    return {"user":temp_user}, 200  

# table populatation -- helper functions 



# reporting query 1 - get count of each event type in stash
@main.route('/transactions/1', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def reporting_1():
    eventTypeData = db.session.query(Stash.stashId, Event.eventType, sqlalchemy.func.count(Event.eventType)).\
        select_from(Event).\
        join(Transaction, Event.transactionId==Transaction.transactionId).\
        join(Stash, Transaction.stashId==Stash.stashId).\
        group_by(Event.eventType, Stash.stashId)

    eventTypeCounts = []
    for event in eventTypeData:
        d = {"stashId": event[0], "eventType": event[1], "count": event[2]}
        eventTypeCounts.append(d)

    return {"data": eventTypeCounts}, 200

# reporting query 2 - get all transactions associated with event type
@main.route('/transactions/2', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def reporting_2():
    stashId = request.args.get('stashId')
    eventType = request.args.get('eventType')

    events = Event.query.filter_by(eventType=eventType).\
        join(Transaction, Event.transactionId==Transaction.transactionId).\
        filter_by(stashId=stashId)

    transactionIds = set()
    for event in events:
        txnId = event.transactionId
        transactionIds.add(int(txnId))

    return {"data": list(transactionIds)}, 200

# reporting query 3 - get all transactions associated with specific user
@main.route('/transactions/3', methods=['GET'])
@cross_origin(origin='*')
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def reporting_3():
    userId = request.args.get('userId')
    
    stashes = Stash.query.filter_by(userId=userId)

    stashIds = []
    for stash in stashes:
        stashIds.append(stash.stashId)

    return {"data": stashIds}, 200

# reporting query 4 - count of function / address pairs in transactions 
@main.route('/transactions/4', methods=['GET'])
@cross_origin(origin='*')
def reporting_4():
    transactionData = db.session.query(Transaction.address, Transaction.function, sqlalchemy.func.count()).\
        select_from(Transaction).\
        group_by(Transaction.address, Transaction.function)

    functionAddressPairs = []
    for transaction in transactionData:
        d = {"address": transaction[0], "function": transaction[1], "count": transaction[2]}
        functionAddressPairs.append(d)

    return {"data": functionAddressPairs}, 200