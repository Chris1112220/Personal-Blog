from app import create_app
from flask_migrate import upgrade

app = create_app()

with app.app_context():
    upgrade()

if __name__ == '__main__':
    app.run(debug=True)
