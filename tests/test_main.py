from app import create_app, db
from app.models import Post


def test_homepage():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        client = app.test_client()
        response = client.get('/')
        assert response.status_code == 200
        assert b'All Posts' in response.data


def test_create_post():
    app = create_app()
    app.config['TESTING'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

        client = app.test_client()
        response = client.post('/create', data={
            'title': 'Test Post',
            'content': 'This is a test post.'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Test Post' in response.data

        post = Post.query.filter_by(title='Test Post').first()
        assert post is not None
        assert post.content == 'This is a test post.'


def test_update_post():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

        post = Post(title='Old Title', content='Old content')
        db.session.add(post)
        db.session.commit()

        client = app.test_client()
        response = client.post(f'/update/{post.id}', data={
            'title': 'New Title',
            'content': 'New content'
        }, follow_redirects=True)

        assert response.status_code == 200

        updated = db.session.get(Post, post.id)
        assert updated.title == 'New Title'
        assert updated.content == 'New content'


def test_delete_post():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

        post = Post(title='Delete Me', content='This will be deleted')
        db.session.add(post)
        db.session.commit()

        client = app.test_client()
        response = client.get(f'/delete/{post.id}', follow_redirects=True)

        assert response.status_code == 200

        deleted = db.session.get(Post, post.id)
        assert deleted is None
