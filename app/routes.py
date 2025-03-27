from flask import Blueprint, render_template, request, redirect, url_for
from .models import Post, db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('view.html', posts=posts)


@main.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create.html')


@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update.html', post=post)


@main.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))
