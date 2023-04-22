from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
#initial commit
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    access = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    comps = db.relationship("Competition",backref="user", lazy=True, cascade = "all, delete-orphan")

    def __init__(self, username, password,access):
        self.username = username
        self.set_password(password)
        self.access = access
        self.is_active = True

    def get_id(self):
        return str(self.id)
        
    def to_json(self):
        return{
            "id": self.id,
            "username": self.username,
            "access": self.access,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def get_access(self):
        return self.access

