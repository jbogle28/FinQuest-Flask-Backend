from app import db 
from flask_bcrypt import generate_password_hash, check_password_hash

completed_scenarios = db.Table('completed_scenarios',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('scenario_id', db.Integer, db.ForeignKey('scenarios.id'), primary_key=True))


class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False) 
    users = db.relationship('User', backref='role', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    xp_total = db.Column(db.Integer, default=0)
    current_level = db.Column(db.Integer, default=1)
    coin_balance = db.Column(db.Numeric(12, 2), default=0.00)

    # --- COSMETIC SYSTEM ---
    
    # This stores the ID of the ONE item currently being worn
    active_cosmetic_id = db.Column(db.Integer, db.ForeignKey('cosmetics.cosmetic_id'), nullable=True)

    # Shortcut to get the actual Cosmetic object the user is wearing
    # Use this to display the profile pic: user.active_item.image_url
    active_item = db.relationship("Cosmetic", foreign_keys=[active_cosmetic_id])

    # Access to the full list of owned items
    owned_cosmetics = db.relationship("UserCosmetic", back_populates="user")

    completed_scenarios = db.relationship('Scenario', secondary=completed_scenarios, backref='completed_by')

    @property
    def level(self):
        return (self.xp_total // 100) + 1
    
    @property
    def xp_in_current_level(self):
        return self.xp_total % 100
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)