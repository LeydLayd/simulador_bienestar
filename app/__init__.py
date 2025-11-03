from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        from app.models import User
        db.create_all()

        if not User.query.first():
            demo_users = [
                User(car_number="TEST001", pin="1111", name="Demo User", balance=100.00)
            ]
            db.session.add_all(demo_users)
            db.session.commit()
            print("✅ Datos de prueba insertados automáticamente.")
        else:
            print("ℹ️ Ya existen datos, no se insertaron duplicados.")

    return app
