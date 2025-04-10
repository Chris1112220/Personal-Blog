from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db

auth_bp = Blueprint('auth', __name__)

ADMIN_USERNAME = "Chris"


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 409

    is_admin = data['username'] == ADMIN_USERNAME
    hashed = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id))
        session['user'] = user.username
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Invalid credentials"}), 401


@auth_bp.route('/login-page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            flash("Login successful.")
            return redirect(url_for('main.index'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('auth.login_page'))
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('main.index'))


@auth_bp.route('/register-page', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("User already exists.")
            return redirect(url_for('auth.register_page'))

        is_admin = username == ADMIN_USERNAME
        hashed = generate_password_hash(password)
        user = User(username=username, password=hashed, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('auth.login_page'))

    return render_template('register.html')
