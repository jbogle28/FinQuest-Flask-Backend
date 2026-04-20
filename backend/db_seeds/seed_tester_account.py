from app import db
from app.models import User, Role, CoinTransaction
from flask_bcrypt import generate_password_hash
from decimal import Decimal

def seed_tester_account():
    # Account Details
    tester_email = "jordanbogle23@gmail.com"
    tester_username = "CREATOR"
    target_xp = 6500 # This results in Level 66 (6500 // 100 + 1)
    target_coins = Decimal("666000.00")
    raw_password = "12345"

    # 1. Ensure the 'Standard' role exists
    standard_role = Role.query.filter_by(role_name='Standard').first()
    if not standard_role:
        standard_role = Role(role_name='Standard')
        db.session.add(standard_role)
        db.session.flush() # Get the role_id before proceeding

    # 2. Find or Create User
    user = User.query.filter_by(email=tester_email).first()
    
    # Generate bcrypt hash
    hashed_pw = generate_password_hash(raw_password).decode('utf8')
    
    if not user:
        print(f"Creating new tester account: {tester_username}")
        user = User(
            username=tester_username,
            email=tester_email,
            f_name="Jordan",
            l_name="Bogle",
            role_id=standard_role.role_id,
            xp_total=target_xp,
            coin_balance=target_coins,
            password_hash=hashed_pw
        )
        db.session.add(user)
    else:
        print(f"Updating existing tester account: {tester_username}")
        user.xp_total = target_xp
        user.coin_balance = target_coins
        user.password_hash = hashed_pw

    db.session.commit()

    # 3. Sync Transaction History for the "CREATOR"
    # We use user.user_id here since the user object is now committed/flushed
    CoinTransaction.query.filter_by(user_id=user.user_id).delete()
    
    initial_tx = CoinTransaction(
        user_id=user.user_id,
        amount=target_coins,
        activity_type="Tester Initialization"
    )
    
    db.session.add(initial_tx)
    db.session.commit()
    
    print(f"Successfully set {tester_username} to XP {target_xp} (Level 66) with {target_coins} coins.")
    print("Password set to: 12345")

if __name__ == "__main__":
    from run import app 
    
    with app.app_context():
        seed_tester_account()