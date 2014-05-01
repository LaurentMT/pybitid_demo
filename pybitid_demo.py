try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse

import uuid
from datetime import datetime
from functools import update_wrapper
from werkzeug.utils import redirect
from flask import Flask
from flask.json import jsonify
from flask.templating import render_template
from flask.helpers import url_for, make_response
from flask.globals import session, request

from pybitid import bitid
from models.user import User
from models.nonce import Nonce
from services.fake_user_db_service import FakeUserDbService
from services.fake_tx_db_service import FakeTxDbService
from services.fake_nonce_db_service import FakeNonceDbService


# Constant indicating if we run the app against Bitcoin test network or main network
USE_TESTNET = False

# Initializes the flask app
app = Flask(__name__)

# Initializes a secret key used to encrypt data in cookies
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

# Initializes services to access databases or services
# For this toy project we use fake dbs storing data in memory
nonce_db_service = FakeNonceDbService()
user_db_service = FakeUserDbService()
tx_db_service = FakeTxDbService()


# NoCache decorator 
# Required to fix a problem with IE which caches all XMLHttpRequest responses 
def nocache(f):
    def add_nocache(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.headers.add('Last-Modified', datetime.now())
        resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        resp.headers.add('Pragma', 'no-cache')
        return resp
    return update_wrapper(add_nocache, f)


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
@nocache
def home():
    params_tpl = {}
    # Checks if user is logged
    if not session.get("uid", None) is None:
        # Gets the user from db
        user = user_db_service.get_user_by_uid(session["uid"])
        if not user is None: params_tpl["user_address"] = user.address
    # Renders the home page
    return render_template('index.html', params_tpl=params_tpl)


@app.route("/login", methods=["GET"])
@nocache
def login():
    '''
    This function initializes the authentication process 
    It builds a challenge which is sent to the client
    '''
    # Initializes a new session id and stores it in the session cookie
    # If user was authenticated, it will be similar to a log out
    session["sid"]  = str(uuid.uuid4())
    session["uid"] = None
    # Creates a new nonce associated to this session
    nonce = Nonce(session["sid"])
    # Stores the nonce in database
    nonce_db_service.create_nonce(nonce)
    # Gets the callback uri
    callback_uri = get_callback_uri()
    # Builds the challenge (bitid uri) 
    bitid_uri = bitid.build_uri(callback_uri, nonce.nid)
    # Gets the qrcode uri
    qrcode = bitid.qrcode(bitid_uri)
    # Renders the login page
    params_tpl = {"callback_uri": callback_uri, "bitid_uri": bitid_uri, "qrcode": qrcode}
    return render_template('login.html', params_tpl=params_tpl)


@app.route("/callback", methods=["POST"])
@nocache
def callback():
    '''
    This function validates the response sent by the client about the challenge
    This is the route called by the bitcoin wallet when the challenge has been signed
    '''
    # Retrieves the callback uri
    callback_uri = get_callback_uri()
    # Extracts data from the posted request (from form of from json data according to the method used by the client)
    container = request.get_json(False, True, False) if request.mimetype == "application/json" else request.form
    bitid_uri = container["uri"]
    signature = container["signature"]
    address   = container["address"]
        
    #
    # Let's start by a bunch of validations
    #
    
    # Checks the address
    if not bitid.address_valid(address, USE_TESTNET):
        return jsonify(message = "Address is invalid or not legal"), 401
    # Checks the bitid uri
    if not bitid.uri_valid(bitid_uri, callback_uri):
        return jsonify(message = "BitID URI is invalid or not legal"), 401
    # Checks the signature
    if not bitid.signature_valid(address, signature, bitid_uri, callback_uri, USE_TESTNET):
        return jsonify(message = "Signature is incorrect"), 401
    
    # Note that the previous 3 steps could also be done in 1 step with following code:
    # if not bitid.challenge_valid(address, signature, bitid_uri, callback_uri, USE_TESTNET):
    #    return jsonify(message = "Sorry but something does not match"), 401
    
    # Checks the nonce
    nid = bitid.extract_nonce(bitid_uri)
    # Tries to retrieve the nonce from db
    nonce = nonce_db_service.get_nonce_by_nid(nid)
    if nonce is None:
        return jsonify(message = "NONCE is illegal"), 401
    elif nonce.has_expired():
        nonce_db_service.delete_nonce(nonce)
        return jsonify(message = "NONCE has expired"), 401
        
    #
    # So good so far, everything seems ok
    # It's time to check if we have a sign out or a sign in
    #
    
    # Checks if a user with the given address has already been registered in db (sign in)
    user = user_db_service.get_user_by_address(address)
    # If we have a sign out
    if user is None:
        # Here, we have an important check to do in order to avoid flooding of the users db
        # Let's check for a proof of goodwill (@see pybitid_demo.services.fake_tx_db_service) 
        if not tx_db_service.check_proof_of_goodwill(address):
            return jsonify(message = "Address is invalid or not legal"), 401
        else:
            # Creates a new user and stores it in db
            user = User(address)
            if not user_db_service.create_user(user):
                return jsonify(message = "Ooops ! Something went wrong but we work on it"), 500
    
    # To finalize the authentication, let's set the user id in the nonce and update it in db
    nonce.uid = user.uid
    if not nonce_db_service.update_nonce(nonce):
        return jsonify(message = "Ooops ! Something went wrong but we work on it"), 500
    # Everything was ok: user is authenticated
    return jsonify(address = address, nonce = nonce.sid)       
            

@app.route("/auth", methods=["GET"])
@nocache
def auth():
    '''
    This function checks if a challenge associated to a given address has been validated
    '''
    # Checks that session id is set
    if not session["sid"]:
        return jsonify(auth = 0)
    # Gets the nonce associated to the session id
    nonce = nonce_db_service.get_nonce_by_sid(session["sid"])
    if nonce is None:
        return jsonify(auth = 0)
    # Checks if nonce has an associated user id
    if nonce.uid is None:
        return jsonify(auth = 0)
    # Gets the user from db
    user = user_db_service.get_user_by_uid(nonce.uid)
    if user is None:
        return jsonify(auth = 0)
    # Let's increase the sign_in counter in user object (for demo purpose only)
    user.signin_count += 1
    user_db_service.update_user(user)
    # Everything is ok, let's finalize the authentication    
    session["uid"] = user.uid
    nonce_db_service.delete_nonce(nonce)
    return jsonify(auth = 1)


@app.route("/user", methods=["GET"])
@nocache
def user():
    # Checks if user is logged
    if session["uid"] is None:
        return redirect(url_for("login")), 401    
    user_address = ""
    user_signin_count = 0
    # Gets the user from db
    user = user_db_service.get_user_by_uid(session["uid"])
    if not user is None:
        user_address = user.address
        user_signin_count = user.signin_count
    params_tpl = {"user_address": user_address, "user_signin_count": user_signin_count}
    return render_template("user.html", params_tpl=params_tpl)


@app.route("/sign_out", methods=["GET"])
@nocache
def sign_out():
    session.pop("uid", None)
    return redirect(url_for("home"))


'''
Utils functions
'''
@app.template_filter("escape_slash")
def escape_slash_filter(s):
    return str.replace(s, "/", "\\/")


def get_callback_uri():
    '''
    Returns the callback uri for this site
    '''
    callback_uri = url_for("home", _external=True)
    parsed = urlparse(callback_uri)
    scheme = parsed.scheme
    netloc = parsed.netloc
    path = "/callback"
    return urlunparse((scheme, netloc, path, "", "", ""))


if __name__ == "__main__":
    # Comment/uncomment following lines to switch production / debug mode
    # Note that using BitId with a smartphone is not possible in debug mode (server only accessible by local machine)
    app.run(host='0.0.0.0')
    #app.run(debug=True)