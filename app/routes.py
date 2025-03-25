from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .models import Post, db
from flask import render_template

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('base.html')


@main.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@main.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    post = Post(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@main.route('/create', methods=['GET'])
def create_view():
    return render_template('create.html')


@main.route('/view', methods=['GET'])
def view_view():
    return render_template('view.html')
