from app import db # Keep only this import
from datetime import datetime, timezone

class AvailableStock(db.Model):
    __tablename__ = 'available_stocks'
    
    stock_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), nullable=False)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    current_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Fundamental Analysis Metrics for the Simulator
    roe_percentage = db.Column(db.Numeric(5, 2))
    debt_to_equity = db.Column(db.Numeric(5, 2))
    profit_margin = db.Column(db.Numeric(5, 2))
    moat_description = db.Column(db.Text)
    intrinsic_value = db.Column(db.Numeric(10, 2))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class AvailableBond(db.Model):
    __tablename__ = 'available_bonds'
    
    bond_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issuer_name = db.Column(db.String(100), nullable=False)
    face_value = db.Column(db.Numeric(10, 2), nullable=False)
    coupon_rate = db.Column(db.Numeric(5, 4), nullable=False) 
    maturity_hours = db.Column(db.Integer, nullable=False)
    risk_rating = db.Column(db.String(10)) 

class UserPortfolio(db.Model):
    __tablename__ = 'user_portfolio'
    
    portfolio_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # Identifying the asset (Polymorphic association)
    asset_id = db.Column(db.Integer, nullable=False)
    asset_type = db.Column(db.String(20), nullable=False) # 'Stock' or 'Bond'
    
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    purchase_price = db.Column(db.Numeric(10, 2), nullable=False)
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow)

# In market.py or wherever your models are defined
class AvailableFD(db.Model):
    __tablename__ = 'available_fds'
    fd_market_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    institution_name = db.Column(db.String(100), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 4), nullable=False) # e.g., 0.08 for 8%
    term_hours = db.Column(db.Integer, default=8) # 8 hours = 1 game year

class FixedDeposit(db.Model):
    __tablename__ = 'fixed_deposits'
    fd_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    fd_market_id = db.Column(db.Integer, db.ForeignKey('available_fds.fd_market_id'), nullable=False)
    principal = db.Column(db.Numeric(10, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 4), nullable=False)
    start_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    end_time = db.Column(db.DateTime, nullable=False)
    # Relationship to get institution name easily
    institution = db.relationship('AvailableFD', backref='user_fds')