import os
from app import create_app, db
from app.models import Cosmetic

# 1. Initialize the app using the factory function
app = create_app()

def seed_cosmetics():
    image_filenames = [
        "otter.png", "panda.png", "koala.png", "lion.png", "kitten.png",
        "knight.png", "chhetah.png", "crown.png", "cut-dog.png", "dragon.png",
        "elephant.png", "goblin.png", "wizard.png", "ruby.png", "sun.png",
        "turtle.png", "baby-duck.png", "bear.png", "bird.png", "python.png",
        "Rhino.png", "rocket.png", "silver-fox.png", "snake.png", "frog.png",
        "gold.png", "ladybug.png", "lambo.png", "monkey.png", "diamond.png",
        "23.png", "ant.png", "black-dog.png", "blob.png", "cash.png", "cat.png"
    ]

    # 2. Use the app context so SQLAlchemy can connect to the DB
    with app.app_context():
        print("Seeding Cosmetics...")
        count = 0
        for filename in image_filenames:
            db_path = f"static/images/cosmetics/{filename}"
            
            if not Cosmetic.query.filter_by(image_url=db_path).first():
                clean_name = filename.rsplit('.', 1)[0].replace('-', ' ').replace('_', ' ').title()
                
                new_item = Cosmetic(
                    name=clean_name,
                    image_url=db_path,
                    price=150
                )
                db.session.add(new_item)
                count += 1
        
        db.session.commit()
        print(f"Success! {count} items added to the store.")

if __name__ == "__main__":
    seed_cosmetics()