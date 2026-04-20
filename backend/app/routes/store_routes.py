from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Cosmetic, UserCosmetic, CoinTransaction

store_bp = Blueprint('store', __name__)

@store_bp.route('/available', methods=['GET'])
@jwt_required()
def get_store():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Get all possible cosmetics
    all_cosmetics = Cosmetic.query.all()
    
    # Get the user's owned item IDs for quick lookup
    owned_ids = [uc.cosmetic_id for uc in user.owned_cosmetics]

    store_list = []
    for c in all_cosmetics:
        store_list.append({
            "id": c.cosmetic_id,
            "name": c.name, # Changed from bg_name to match updated model
            "image": c.image_url,
            "cost": c.price, # Changed from cost to price to match updated model
            "owned": c.cosmetic_id in owned_ids,
            "equipped": c.cosmetic_id == user.active_cosmetic_id
        })
    
    return jsonify(store_list), 200

@store_bp.route('/purchase', methods=['POST'])
@jwt_required()
def buy_background():
    user_id = get_jwt_identity()
    cosmetic_id = request.json.get('cosmetic_id')
    
    user = User.query.get(user_id)
    item = Cosmetic.query.get(cosmetic_id)
    
    # 1. Validation
    if not item: 
        return jsonify({"msg": "Item not found"}), 404
    
    # Check if already owned via relationship
    already_owned = UserCosmetic.query.filter_by(user_id=user_id, cosmetic_id=cosmetic_id).first()
    if already_owned: 
        return jsonify({"msg": "Already owned"}), 400
    
    if user.coin_balance < item.price:
        return jsonify({"msg": "Insufficient coins"}), 400

    # 2. Deduction & Transaction Log
    user.coin_balance -= item.price
    
    # Add to inventory
    new_purchase = UserCosmetic(user_id=user_id, cosmetic_id=cosmetic_id)
    
    tx = CoinTransaction(
        user_id=user_id,
        amount=-float(item.price), 
        activity_type=f"Store: {item.name}"
    )
    
    db.session.add(new_purchase)
    db.session.add(tx)
    db.session.commit()
    
    return jsonify({
        "msg": "Purchase successful!", 
        "balance": float(user.coin_balance)
    }), 200

@store_bp.route('/equip', methods=['POST'])
@jwt_required()
def equip_background():
    user_id = get_jwt_identity()
    cosmetic_id = request.json.get('cosmetic_id')
    
    user = User.query.get(user_id)

    # 1. Verify ownership
    ownership = UserCosmetic.query.filter_by(user_id=user_id, cosmetic_id=cosmetic_id).first()
    if not ownership:
        return jsonify({"msg": "You do not own this item"}), 403
    
    # 2. Update the User's single active slot
    # This automatically "unequips" the old one because the column can only hold one ID
    user.active_cosmetic_id = cosmetic_id
    db.session.commit()
    
    return jsonify({
        "msg": "Item equipped!", 
        "active_cosmetic_id": user.active_cosmetic_id
    }), 200

@store_bp.route('/my-inventory', methods=['GET'])
@jwt_required()
def get_user_inventory():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # We access the user's inventory through the relationship
    # 'uc.cosmetic' gives us the actual details (name, url) from the Cosmetic table
    inventory = []
    for uc in user.owned_cosmetics:
        item = uc.cosmetic
        inventory.append({
            "cosmetic_id": item.cosmetic_id,
            "name": item.name,
            "image_url": item.image_url,
            "is_active": item.cosmetic_id == user.active_cosmetic_id
        })

    return jsonify({
        "count": len(inventory),
        "inventory": inventory
    }), 200