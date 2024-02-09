from flask import Blueprint, render_template, request, redirect, url_for

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Procesar el formulario
        return redirect(url_for('frontend.index'))
    return render_template('login.html')