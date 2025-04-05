from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Post, db
from functools import wraps

main = Blueprint('main', __name__)

# Decorator to protect routes


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to access this page.")
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Homepage - view all posts


@main.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('view.html', posts=posts)

# Create post - protected


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create.html')

# Update post - protected


@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update.html', post=post)

# Delete post - protected


@main.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))
