from app import create_app, db
from app.models.user import Role

app = create_app()

def seed_roles():
    with app.app_context():
        print("Checking for 'Standard' role...")
        
        # Check if it already exists to avoid duplicates
        existing_role = Role.query.filter_by(role_name='Standard').first()
        
        if not existing_role:
            new_role = Role(role_name='Standard')
            db.session.add(new_role)
            db.session.commit()
            print("Successfully added 'Standard' role!")
        else:
            print("Role 'Standard' already exists in the database.")

if __name__ == "__main__":
    seed_roles()