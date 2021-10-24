from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref
import uuid
import secrets


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)



class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    superpower = db.Column(db.String(50))
    human_alien = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)



    def __init__(self, name, description, superpower, human_alien, user_token, id = ' '):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.superpower = superpower
        self.human_alien = human_alien
        self.user_token = user_token


    def set_id(self):
        return (secrets.token_urlsafe())



class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id','name','description','superpower','human_alien']

hero_schema = HeroSchema()
heros_schema = HeroSchema(many = True)