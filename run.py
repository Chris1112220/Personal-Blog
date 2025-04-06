from app import create_app
from flask_migrate import upgrade
from flask import request, redirect

app = create_app()


@app.before_request
def enforce_https():
    if not request.is_secure and not app.debug:
        url = request.url.replace("http://", "https://", 1)
        return redirect(url)


with app.app_context():
    upgrade()


if __name__ == '__main__':
    app.run(debug=True)
