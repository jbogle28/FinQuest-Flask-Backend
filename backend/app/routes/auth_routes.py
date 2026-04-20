import logging
from flask import Blueprint, request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_jwt_extended import create_access_token, jwt_required
from flask_mail import Message
from app import mail 
from app.extensions import db
from app.models.user import User, Role
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import get_jwt_identity
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
from app.models import Cosmetic, UserCosmetic, CoinTransaction
from sqlalchemy import func, and_
from datetime import timedelta, datetime

# Configure logging to see errors in your terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"msg": "Request body must be JSON"}), 400

        # Validate mandatory fields
        required = ['username', 'email', 'password', 'f_name', 'l_name']
        if not all(field in data for field in required):
            return jsonify({"msg": "Missing required fields"}), 400

        # Check for existing user
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"msg": "Username already taken"}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"msg": "Email already registered"}), 409

        # Assign Default Role
        role = Role.query.filter_by(role_name='Standard').first()
        
        # 1. Find the starter avatar
        starter_avatar = Cosmetic.query.filter_by(name="Cat").first()

        new_user = User(
            f_name=data['f_name'],
            l_name=data['l_name'],
            username=data['username'],
            email=data['email'],
            role_id=role.role_id if role else 1,
            # 2. Set the active ID right here
            active_cosmetic_id=starter_avatar.cosmetic_id if starter_avatar else None
        )
        
        # Requirement 2.2: Secure Hashing
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        
        # 3. Flush allows us to get the new user_id without finishing the transaction yet
        db.session.flush()

        # 4. Add the starter avatar to the user's inventory
        if starter_avatar:
            user_inventory_entry = UserCosmetic(
                user_id=new_user.user_id, 
                cosmetic_id=starter_avatar.cosmetic_id
            )
            db.session.add(user_inventory_entry)

        db.session.commit()
        try:
            msg = Message(
                "Welcome to FinQuest!",
                recipients=[new_user.email],
                body=f"Hi {new_user.f_name},\n\nWelcome to FinQuest! Your account has been created successfully. Start your journey to financial literacy today!"
            )

            mail.send(msg)
        except Exception as e:
            # We log the error but don't stop registration if the email fails
            logger.error(f"Failed to send welcome email: {e}")

        return jsonify({"msg": "Registration successful"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Requirement 1.1.2: Authenticate and generate 12hr token"""
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"msg": "Username and password required"}), 400

        user = User.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            token = create_access_token(identity=str(user.user_id))
            
            return jsonify({
                "access_token": token,
                "user": {
                    "username": user.username,
                    "f_name": user.f_name,
                    "role": user.role.role_name if user.role else "Standard",
                    "xp_total": user.xp_total,
                    "coin_balance": float(user.coin_balance) # Added this!
                }
            }), 200
            
        return jsonify({"msg": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"msg": "Login failed", "error": str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"msg": "Logged out successfully"}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(email, salt='password-reset-salt')
        
        # FIX: Point this to your React App (Port 3000), NOT the Flask API
        # In production, this would be 'https://finquest.com/reset-password/'
        frontend_base_url = "http://localhost:3000/reset-password"
        reset_url = f"{frontend_base_url}/{token}"

        msg = Message("FinQuest: Password Reset Request",
                      recipients=[email])
        msg.body = f"Click the link to reset your password: {reset_url}\nIf you did not request this, ignore this email."
        mail.send(msg)

    # Always return success to prevent email harvesting
    return jsonify({"msg": "If that email exists, a reset link has been sent."}), 200


@auth_bp.route('/reset-password-confirm', methods=['POST'])
def reset_password_confirm():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')

        if not token or not new_password:
            return jsonify({"msg": "Token and password are required"}), 400

        # Ensure SECRET_KEY is loaded
        secret_key = current_app.config.get('SECRET_KEY')
        if not secret_key:
            logger.error("SECRET_KEY is not configured in the app config.")
            return jsonify({"msg": "Server configuration error"}), 500

        serializer = URLSafeTimedSerializer(secret_key)
        
        try:
            # Token expires in 1800 seconds (30 minutes)
            email = serializer.loads(token, salt='password-reset-salt', max_age=1800)
        except SignatureExpired:
            return jsonify({"msg": "The reset link has expired."}), 400
        except BadSignature:
            return jsonify({"msg": "Invalid reset link."}), 400

        user = User.query.filter_by(email=email).first()
        
        if user:
            try:
                user.set_password(new_password) 
                db.session.commit()
                return jsonify({"msg": "Your password has been updated successfully!"}), 200
            except Exception as e:
                db.session.rollback()
                logger.error(f"Database commit failed: {str(e)}")
                return jsonify({"msg": "Failed to update password in database"}), 500

        return jsonify({"msg": "User account no longer exists."}), 404

    except Exception as e:
        logger.error(f"Unexpected error in reset_confirm: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500


def generate_reset_token(email):
    # This will now throw a clear error if SECRET_KEY is missing
    secret_key = current_app.config.get('SECRET_KEY')
    if not secret_key:
        raise ValueError("SECRET_KEY is missing from Flask configuration")
        
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt='password-reset-salt')

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_data():
    """Requirement: Fetch full profile for Navbar/Dashboard"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))

        if not user:
            return jsonify({"msg": "User not found"}), 404

        return jsonify({
            "user": {
                "f_name": user.f_name,
                "l_name": user.l_name,
                "username": user.username,
                "email": user.email,
                "role": user.role.role_name if user.role else "Standard",
                "xp_total": user.xp_total,
                "coin_balance": float(user.coin_balance),
                "current_level": (user.xp_total // 100) + 1,
                "xp_percent": user.xp_total % 100,
                # Include the ID for the logic in ProfileSettings.jsx
                "active_cosmetic_id": user.active_cosmetic_id,
                # Provide the direct URL for the Navbar and top profile div
                "profile_image": user.active_item.image_url if user.active_item else None
            }
        }), 200
    except Exception as e:
        return jsonify({"msg": "Failed to fetch user", "error": str(e)}), 500

@auth_bp.route('/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    """Returns all users sorted by XP (descending) for the leaderboard"""
    try:
        # Sort by xp_total highest to lowest
        users = User.query.order_by(User.xp_total.desc(), User.username.asc()).all()

        leaderboard_data = []
        for index, user in enumerate(users):
            leaderboard_data.append({
                "rank": index + 1,
                "username": user.username,
                "xp_total": user.xp_total,
                "level": (user.xp_total // 100) + 1,
                "coin_balance": float(user.coin_balance),
                "role": user.role.role_name if user.role else "Standard",
                # Add the avatar URL so it shows up next to names on the leaderboard
                "avatar_url": user.active_item.image_url if user.active_item else None
            })

        return jsonify(leaderboard_data), 200

    except Exception as e:
        return jsonify({"msg": "Failed to fetch leaderboard", "error": str(e)}), 500

@auth_bp.route('/leaderboard/wealth', methods=['GET'])
@jwt_required()
def get_wealth_leaderboard():
    """Returns users ranked by Coin balance and 48h earnings"""
    try:
        # Time window: last 48 hours
        time_threshold = datetime.utcnow() - timedelta(hours=48)

        # Subquery to calculate earnings in the last 48h per user
        recent_earnings = db.session.query(
            CoinTransaction.user_id,
            func.sum(CoinTransaction.amount).label('recent_sum')
        ).filter(
            CoinTransaction.created_at >= time_threshold,
            CoinTransaction.amount > 0 # Only count income, not purchases
        ).group_by(CoinTransaction.user_id).subquery()

        # Join User with the earnings subquery
        users = db.session.query(User, recent_earnings.c.recent_sum).outerjoin(
            recent_earnings, User.user_id == recent_earnings.c.user_id
        ).order_by(User.coin_balance.desc()).all()

        leaderboard_data = []
        for index, (user, earnings) in enumerate(users):
            leaderboard_data.append({
                "rank": index + 1,
                "username": user.username,
                "coin_balance": float(user.coin_balance),
                "recent_earnings": float(earnings) if earnings else 0.0,
                "level": (user.xp_total // 100) + 1, # Adding Level calculation
                "role": user.role.role_name if user.role else "Standard",
                "avatar_url": user.active_item.image_url if user.active_item else None
            })

        return jsonify(leaderboard_data), 200

    except Exception as e:
        logger.error(f"Wealth Leaderboard Error: {e}")
        return jsonify({"msg": "Failed to fetch wealth leaderboard"}), 500

@auth_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Update only allowed fields
    if 'f_name' in data:
        user.f_name = data['f_name']
    if 'l_name' in data:
        user.l_name = data['l_name']

    try:
        db.session.commit()
        return jsonify({"msg": "Profile updated!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to update", "error": str(e)}), 500
    

