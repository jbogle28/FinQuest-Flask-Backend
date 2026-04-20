from app import db

class Cosmetic(db.Model):
    __tablename__ = 'cosmetics'
    
    cosmetic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)      # e.g., 'Golden Dragon'
    image_url = db.Column(db.String(255), nullable=False) # e.g., 'static/assets/dragon.png'
    price = db.Column(db.Integer, nullable=False)        # Price in coins

    # Relationship to see which users own this
    owners = db.relationship('UserCosmetic', back_populates='cosmetic')


class UserCosmetic(db.Model):
    __tablename__ = 'user_cosmetics'
    
    # Simple linking table for ownership inventory
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    cosmetic_id = db.Column(db.Integer, db.ForeignKey('cosmetics.cosmetic_id'), primary_key=True)
    
    # Relationships to link back to the main objects
    user = db.relationship("User", back_populates="owned_cosmetics")
    cosmetic = db.relationship("Cosmetic", back_populates="owners")