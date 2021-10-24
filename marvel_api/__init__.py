from flask import Flask
from config import Config
from .authentication.routes import auth
from .site.routes import site
from flask_migrate import Migrate
from .models import db, login_manager, ma
from flask_cors import CORS
from .api.routes import api




app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)


CORS(app)


db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)

login_manager.login_view = 'auth.signin'
migrate = Migrate(app, db)

