from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory
from .models import Post, Comment, User, db
from functools import wraps
import os

main = Blueprint('main', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to access this page.")
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function


def is_admin():
    user = User.query.filter_by(username=session.get('user')).first()
    return user and user.is_admin


@main.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    comments = Comment.query.order_by(Comment.date_posted.asc()).all()
    return render_template('view.html', posts=posts, comments=comments)


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not is_admin():
        flash("Only the site owner can create posts.")
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create.html')


@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if not is_admin():
        flash("Only the site owner can edit posts.")
        return redirect(url_for('main.index'))
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update.html', post=post)


@main.route('/delete/<int:id>')
@login_required
def delete(id):
    if not is_admin():
        flash("Only the site owner can delete posts.")
        return redirect(url_for('main.index'))
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    content = request.form['content']
    username = session.get('user')
    new_comment = Comment(content=content, post_id=post_id, username=username)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/google74550b9db6d52a16.html')
def google_verify():
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), '..', 'static'),
        'google74550b9db6d52a16.html'
    )
