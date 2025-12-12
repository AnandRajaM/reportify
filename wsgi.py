"""
Flask WSGI Application Entry Point
Run with: python wsgi.py
For production: gunicorn wsgi:app
"""
from flask import Flask
from app.web.routes import web_bp
from app.core.config import settings

# Initialize Flask app
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

app.config['SECRET_KEY'] = 'your-secret-key-here'  # change w/ prod
app.config['DEBUG'] = settings.DEBUG

# Register blueprints
app.register_blueprint(web_bp)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=settings.DEBUG
    )
