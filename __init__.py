# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
from sched import scheduler
import time
from flask import Flask
import sqlalchemy
from Aclient import Aclient
from OracleClient import OracleClient
from flask_apscheduler import APScheduler
from models import *
# Flask constructor takes the name of
# current module (__name__) as argument.
NODE_URL = "https://fullnode.mainnet.aptoslabs.com/v1"

escapedPassword = urllib.parse.quote_plus(os.environ.get("DB_PASSWORD"))
sqldialect = os.environ.get("DB_DIALECT")
username = os.environ.get("DB_USER")
database = os.environ.get("DB_NAME")
host = os.environ.get("DB_HOST")
key = os.environ.get("DB_SECRET_KEY")
connectionString = f"{sqldialect}://{username}:{escapedPassword}@{host}/{database}?ssl_key=MyCertFolder/client-key.pem&ssl_cert=MyCertFolder/client-cert.pem"
sqlUrl = sqlalchemy.engine.url.URL(
    drivername="mysql+pymysql",
    username=username,
    password=escapedPassword,
    host=host,
    port=3306,
    database=database,
    query={"ssl_ca": "/etc/ssl/cert.pem"},
)
db = SQLAlchemy()
app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

aClient = Aclient(NODE_URL)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	return 'Hello World'

oc = OracleClient()


@scheduler.task('interval', id='oracle_manager', seconds=100, misfire_grace_time=900)
def oracle_update():
    with app.app_context():
        print("Running oracle manager")
        # stopwatch = time.time()
        
        new_prices = oc.update_switchboard()
        for price in new_prices:
            print("PRICE",price)
            # o = Oracle(
            #     oracleName=price[0]+"_switchboard",
            #     price=price[1],
            #     timestamp=price[2])
            # # check if this oracle already exists
            # oracle = Oracle.query.filter_by(oracleName=o.oracleName, timestamp=price[2]).first()
        #     print("Oracle", oracle)
        #     if oracle is None:
        #         db.session.add(o)
        # db.session.commit()
with app.app_context():
    user = User()
    wallet = Wallet()
    # dapp = Dapp()
    db.create_all()

# def spot_prices('/spot_prices'):
# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()


