from flask import Blueprint, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
import requests

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
@jwt_required(optional=True)
def index():
    current_user = get_jwt_identity()
    if current_user:
        return redirect(url_for('frontend.frontend.test'))
    else:
        return redirect(url_for('frontend.frontend.login'))

@frontend.route('/login', methods=['GET', 'POST'])
@jwt_required(optional=True)
def login():
    current_user = get_jwt_identity()
    if current_user:
        return redirect(url_for('frontend.frontend.test'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            token = requests.post('http://localhost/api/login', json={'username': username, 'password': password}).json()
            if 'access_token' in token:
                resp = redirect(url_for('frontend.frontend.test'))
                set_access_cookies(resp, token['access_token'])
                return resp
            else:
                return render_template('login.html', error='Incorrect username or password')

        return render_template('login.html')

@frontend.route('/logout', methods=['GET'])
def logout():
    resp = redirect(url_for('frontend.frontend.login'))
    unset_jwt_cookies(resp)
    return resp

@frontend.route('/register', methods=['GET', 'POST'])
@jwt_required(optional=True)
def register():
    current_user = get_jwt_identity()
    if current_user:
        return redirect(url_for('frontend.frontend.test'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            resp = requests.post('http://localhost/api/users', json={'username': username, 'password': password})
            if resp.status_code == 201:
                return redirect(url_for('frontend.frontend.login'))
            elif resp.status_code == 400:
                return render_template('register.html', error='User already exists')
            else:
                return render_template('register.html', error='Unexpected error')

        return render_template('register.html')

@frontend.route('/test', methods=['GET'])
@jwt_required(optional=True) 
def test():
    current_user = get_jwt_identity()
    if current_user:
        return render_template('test.html', user=current_user)
    else:
        return render_template('test.html', user='Anónimo')