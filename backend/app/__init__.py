import os
from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, bcrypt, jwt, migrate 
from flask_mail import Mail

# 1. Initialize extensions globally
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(Config)

    # 2. Initialize extensions with the app
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Better for production
    CORS(app, resources={r"/*": {"origins": [
        "http://localhost:3000", 
        "https://your-finquest-frontend.vercel.app"
    ]}}, supports_credentials=True)
    # 4. Import models within app context
    with app.app_context():
        from app.models.user import User, Role, completed_scenarios
        from app.models.economy import CoinTransaction, Investment
        # Add CrosswordEntry here so it's included in migrations/metadata
        from app.models.game import QuizQuestion, VocabularyTerm, GameHistory, CrosswordEntry
        from app.models.cosmetics import Cosmetic, UserCosmetic
        from app.models.market import AvailableStock, AvailableBond, UserPortfolio

    # 5. Register Blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.quiz_routes import quiz_bp
    app.register_blueprint(quiz_bp, url_prefix='/quiz')

    from app.routes.game_routes import game_bp
    app.register_blueprint(game_bp, url_prefix='/game')

    from app.routes.finance_routes import finance_bp
    app.register_blueprint(finance_bp, url_prefix='/finance')

    from app.routes.store_routes import store_bp
    app.register_blueprint(store_bp, url_prefix='/api/store')

    return app