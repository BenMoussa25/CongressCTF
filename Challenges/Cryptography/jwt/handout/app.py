import jwt
from flask import Flask, render_template, request, redirect, url_for, make_response, g
from datetime import datetime, timedelta
from functools import wraps
from secret import FLAG , ADMINPASS
from time import sleep


app = Flask(__name__)

PRIVATE_KEY_PATH = 'keys/private.pem'
PUBLIC_KEY_PATH = 'keys/public.pem'

USER = "spark"
PASS = ADMINPASS

file = open(PUBLIC_KEY_PATH,'r')
PUBLIC_KEY = file.read()
file = open(PRIVATE_KEY_PATH,'r')
PRIVATE_KEY = file.read()

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            token = request.cookies.get('token')
            if not token:
                return "<h1>Unauthorized access! Please log in.</h1>"
            try:
                decoded = (jwt.decode(token, PUBLIC_KEY, algorithms=['RS256' , 'HS256']))
                g.user = decoded['username']
                g.role = decoded['role']
                if role and g.role != role:
                    return "<h1>Access denied. You are not authorized to view this page.</h1>"
            except jwt.ExpiredSignatureError:
                return "<h1>Token has expired. Please log in again.</h1>"
            except jwt.InvalidTokenError:
                return "<h1>Invalid token. Please log in again.</h1>"
            return f(*args, **kwargs)
        return wrapped
    return decorator


def is_equal(a, b):
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            return False
        sleep(0.02)

    if len(a) != len(b):
        return False

    return True
        

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == USER and is_equal(password, PASS):
        payload = {
            'username': username,
            'role': 'player',
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')

        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('token', token.decode(), httponly=True, samesite='Strict')
        return resp
    
    return "<h1>Invalid Credentials. Please try again.</h1>"

@app.route('/dashboard')
@token_required()
def dashboard():
    return f"<h1>Welcome to your dashboard, {g.user}! Your role is: {g.role}.</h1>"

@app.route('/admin')
@token_required(role='admin')
def admin():
    return "<h1>Welcome to the admin page!</h1>\n" + FLAG.decode()

@app.route('/logout')
def logout():
    resp = make_response("<h1>You have been logged out.</h1>")
    resp.delete_cookie('token')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
