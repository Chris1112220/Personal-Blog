from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .models import Post, db

main = Blueprint('main', __name__)


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
