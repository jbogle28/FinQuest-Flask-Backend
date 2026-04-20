from app import db
from app.models.market import AvailableFD, FixedDeposit
from run import app

def seed_fd_market():
    # 1. Clear existing data to avoid duplicates or "One FD per Institution" conflicts
    print("Clearing old Fixed Deposit data...")
    FixedDeposit.query.delete() # Clear user deposits first due to FK constraints
    AvailableFD.query.delete()
    db.session.commit()

    # 2. Define expanded Jamaican Institutional Data
    # 8 hours = 1 game year. 4h = 6 months. 24h = 3 years.
    institutions = [
        {
            "name": "NCB (National Coin Bank)", 
            "rate": 0.0450, 
            "term": 2
        },
        {
            "name": "JN FinQuest Savings", 
            "rate": 0.15, 
            "term": .1
        },
        {
            "name": "Sagicor SmartSaver (Short-Term)", 
            "rate": 0.0210, 
            "term": 4 # 6 months in-game
        },
        {
            "name": "Scotia Digital Vault", 
            "rate": 0.0480, 
            "term": 6
        },
        {
            "name": "Victoria Mutual Fixed", 
            "rate": 0.0550, 
            "term": 8
        },
        {
            "name": "JMMB Goal-Getter (Long-Term)", 
            "rate": 0.1850, 
            "term": 24 # 3 years in-game
        },
        {
            "name": "Barita Alpha Fund", 
            "rate": 0.0820, 
            "term": 8
        }
    ]
    
    print("Seeding new Fixed Deposit market...")
    for inst in institutions:
        new_offer = AvailableFD(
            institution_name=inst['name'],
            interest_rate=inst['rate'],
            term_hours=inst['term']
        )
        db.session.add(new_offer)
    
    try:
        db.session.commit()
        print(f"Successfully seeded {len(institutions)} institutions.")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")

if __name__ == "__main__":
    with app.app_context():
        seed_fd_market()