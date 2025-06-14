from flask import Flask
from config import Config
from models import db
from models.user import User
from models.task import Task
from routes.auth_routes import auth
from routes.task_routes import task_bp
from flask_login import LoginManager
from routes.admin_routes import admin_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')

# ✅ Bind SQLAlchemy กับ app
db.init_app(app)

# หลังจาก db.init_app(app)
migrate = Migrate(app, db)

# ✅ Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(task_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()