# Contains endpoints for Fixed Deposits, buying Bonds, and trading Stocks.
import random
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.market import AvailableFD
from app.models import (
    User,
    FixedDeposit,
    AvailableBond, 
    AvailableStock, 
    UserPortfolio, 
    CoinTransaction
)
from datetime import datetime, timedelta
from decimal import Decimal

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/bonds/market', methods=['GET'])
@jwt_required()
def get_bond_market():
    # Allow users to browse available bonds
    bonds = AvailableBond.query.all()
    market_data = []
    for b in bonds:
        market_data.append({
            "id": b.bond_id,
            "issuer": b.issuer_name,
            "price": float(b.face_value),
            "coupon_rate": f"{float(b.coupon_rate * 100)}%", # e.g. 8.5%
            "duration_hours": b.maturity_hours,
            "risk": b.risk_rating
        })
    return jsonify(market_data), 200

@finance_bp.route('/bonds/purchase', methods=['POST'])
@jwt_required()
def purchase_bond():
    user_id = get_jwt_identity()
    bond_id = request.json.get('bond_id')
    quantity = request.json.get('quantity', 1) # Usually 1 for bonds
    
    user = User.query.get(user_id)
    bond = AvailableBond.query.get(bond_id)
    
    if not bond: return jsonify({"msg": "Bond not found"}), 404
    
    total_cost = bond.face_value * quantity
    
    # Check if user can afford it
    if user.coin_balance < total_cost:
        return jsonify({"msg": "Insufficient coins"}), 400
        
    # 1. Deduct Coins & Log Transaction (Requirement 1.4)
    user.coin_balance -= total_cost
    tx = CoinTransaction(
        user_id=user_id,
        amount=-total_cost,
        activity_type=f"Bond Purchase: {bond.issuer_name}"
    )
    
    # 2. Add to Portfolio (Requirement 1.8)
    new_holding = UserPortfolio(
        user_id=user_id,
        asset_id=bond.bond_id,
        asset_type='Bond',
        quantity=quantity,
        purchase_price=bond.face_value,
        purchased_at=datetime.utcnow()
    )
    
    db.session.add(tx)
    db.session.add(new_holding)
    db.session.commit()
    
    return jsonify({
        "msg": "Bond purchased successfully!",
        "new_balance": float(user.coin_balance)
    }), 200
# Helper to calculate Margin of Safety
def calculate_mos(current, intrinsic):
    if not intrinsic or intrinsic <= 0: return 0
    # Formula: ((Intrinsic - Current) / Intrinsic) * 100
    mos = ((intrinsic - current) / intrinsic) * 100
    return round(float(mos), 2)

@finance_bp.route('/stocks/market', methods=['GET'])
@jwt_required()
def get_stock_market():
    stocks = AvailableStock.query.all()

    for s in stocks:
        simulate_market_movements(s)

    market_data = []
    
    for s in stocks:
        market_data.append({
            "id": s.stock_id,
            "ticker": s.ticker,
            "company": s.company_name,
            "price": float(s.current_price),
            "metrics": {
                "roe": f"{s.roe_percentage}%",
                "debt_to_equity": float(s.debt_to_equity),
                "profit_margin": f"{s.profit_margin}%",
                "moat": s.moat_description
            },
            "margin_of_safety": calculate_mos(s.current_price, s.intrinsic_value),
            "intrinsic_value": float(s.intrinsic_value)
        })
    return jsonify(market_data), 200

@finance_bp.route('/stocks/trade', methods=['POST'])
@jwt_required()
def trade_stock():
    user_id = get_jwt_identity()
    data = request.json
    stock_id = data.get('stock_id')
    action = data.get('action') # 'BUY' or 'SELL'
    quantity = Decimal(str(data.get('quantity', 0)))
    
    user = User.query.get(user_id)
    stock = AvailableStock.query.get(stock_id)
    
    if not stock or quantity <= 0:
        return jsonify({"msg": "Invalid trade parameters"}), 400

    total_value = stock.current_price * quantity

    if action == 'BUY':
        if user.coin_balance < total_value:
            return jsonify({"msg": "Insufficient coins"}), 400
        
        user.coin_balance -= total_value
        # Add to Portfolio
        new_holding = UserPortfolio(
            user_id=user_id, asset_id=stock_id, asset_type='Stock',
            quantity=quantity, purchase_price=stock.current_price
        )
        db.session.add(new_transaction(user_id, -total_value, f"Bought {stock.ticker}"))
        db.session.add(new_holding)

    elif action == 'SELL':
        # Check if they own enough shares
        holding = UserPortfolio.query.filter_by(
            user_id=user_id, asset_id=stock_id, asset_type='Stock'
        ).first()
        
        if not holding or holding.quantity < quantity:
            return jsonify({"msg": "Not enough shares to sell"}), 400
        
        user.coin_balance += total_value
        holding.quantity -= quantity
        
        if holding.quantity == 0:
            db.session.delete(holding)
            
        db.session.add(new_transaction(user_id, total_value, f"Sold {stock.ticker}"))

    db.session.commit()
    return jsonify({"msg": f"Successfully {action.lower()}ed {quantity} shares"}), 200

# Helper for transactions
def new_transaction(u_id, amt, act):
    return CoinTransaction(user_id=u_id, amount=amt, activity_type=act)


@finance_bp.route('/portfolio/details', methods=['GET'])
@jwt_required()
def get_portfolio_details():
    user_id = get_jwt_identity()
    holdings = UserPortfolio.query.filter_by(user_id=user_id).all()
    
    portfolio_items = []
    total_invested = 0
    current_market_value = 0

    for h in holdings:
        if h.asset_type == 'Stock':
            s = AvailableStock.query.get(h.asset_id)
            if not s: continue
            current_val = float(s.current_price) * float(h.quantity)
            initial_cost = float(h.purchase_price) * float(h.quantity)
            
            total_invested += initial_cost
            current_market_value += current_val
            
            portfolio_items.append({
                "id": h.portfolio_id,
                "asset_id": s.stock_id,
                "type": "Stock",
                "name": s.company_name,
                "ticker": s.ticker,
                "qty": float(h.quantity),
                "avg_price": float(h.purchase_price),
                "current_price": float(s.current_price),
                "profit_loss": current_val - initial_cost,
                "pl_percentage": ((current_val - initial_cost) / initial_cost * 100) if initial_cost > 0 else 0
            })
        
        elif h.asset_type == 'Bond':
            b = AvailableBond.query.get(h.asset_id)
            if not b: continue
            current_val = float(b.face_value) * float(h.quantity)
            total_invested += current_val
            current_market_value += current_val
            
            portfolio_items.append({
                "id": h.portfolio_id,
                "asset_id": b.bond_id,
                "type": "Bond",
                "name": b.issuer_name,
                "qty": float(h.quantity),
                "price": float(b.face_value),
                "coupon": f"{float(b.coupon_rate * 100)}%",
                "risk": b.risk_rating
            })

    return jsonify({
        "items": portfolio_items,
        "summary": {
            "total_invested": round(total_invested, 2),
            "market_value": round(current_market_value, 2),
            "net_position": round(current_market_value - total_invested, 2)
        }
    }), 200


@finance_bp.route('/stocks/tick', methods=['POST'])
def simulate_market_movements(stock):
    now = datetime.utcnow()
    # Calculate how many 5-minute intervals have passed
    minutes_passed = (now - stock.last_updated).total_seconds() / 60
    ticks_to_run = int(minutes_passed // 5) # One tick every 5 minutes

    if ticks_to_run > 0:
        current_price = float(stock.current_price)
        intrinsic = float(stock.intrinsic_value)
        
        for _ in range(ticks_to_run):
            # 1. Pull toward Intrinsic Value (Gravity)
            # If price is way above intrinsic, it's more likely to drop
            gravity = (intrinsic - current_price) * 0.01
            
            # 2. Random Volatility (Noise)
            noise = random.uniform(-0.02, 0.02) * current_price
            
            # 3. Update Price
            current_price += (gravity + noise)
            
        stock.current_price = round(Decimal(str(current_price)), 2)
        stock.last_updated = now
        db.session.commit()

# --- FIXED DEPOSIT ROUTES ---

@finance_bp.route('/fd/status', methods=['GET'])
@jwt_required()
def get_fd_status():
    user_id = get_jwt_identity()
    active_fds = FixedDeposit.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        "id": fd.fd_id, # Changed to "id" to match frontend mapping
        "institution": fd.institution.institution_name,
        "principal": float(fd.principal),
        "end_time": fd.end_time.isoformat(),
        "interest_rate": float(fd.interest_rate) # Changed to match frontend naming
    } for fd in active_fds]), 200

@finance_bp.route('/fd/market', methods=['GET'])
@jwt_required()
def get_fd_market():
    fds = AvailableFD.query.all()
    return jsonify([{
        "id": f.fd_market_id,
        "institution": f.institution_name,
        "rate": float(f.interest_rate),
        "term": f.term_hours
    } for f in fds]), 200

@finance_bp.route('/fd/create', methods=['POST'])
@jwt_required()
def create_fd():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Use .get() and check for None explicitly to allow ID 0 or floats
    market_id = data.get('market_id')
    raw_amount = data.get('amount')

    # FIX: "not market_id" fails if ID is 0. Use "is None" instead.
    if market_id is None or raw_amount is None:
        return jsonify({"msg": "Missing investment details."}), 400

    try:
        amount = Decimal(str(raw_amount))
        if amount <= 0:
            return jsonify({"msg": "Investment amount must be greater than 0."}), 400
    except Exception:
        return jsonify({"msg": "Invalid amount format."}), 400
    
    # Check if the offering exists before checking for duplicates
    offering = AvailableFD.query.get(market_id)
    if not offering:
        return jsonify({"msg": "Selected investment plan no longer available."}), 404
    
    # Check for existing deposit with this specific institution
    existing = FixedDeposit.query.filter_by(user_id=user_id, fd_market_id=market_id).first()
    if existing:
        return jsonify({"msg": f"You already have an active deposit with {offering.institution_name}."}), 400

    user = User.query.get(user_id)
    if user.coin_balance < amount:
        return jsonify({"msg": "Insufficient coins to open this deposit."}), 400

    finish_time = datetime.utcnow() + timedelta(hours=offering.term_hours)
    
    try:
        new_fd = FixedDeposit(
            user_id=user_id,
            fd_market_id=market_id,
            principal=amount,
            interest_rate=offering.interest_rate,
            end_time=finish_time
        )

        # Deduct balance and log transaction
        user.coin_balance -= amount
        db.session.add(CoinTransaction(
            user_id=user_id, 
            amount=-amount, 
            activity_type=f"FD Open: {offering.institution_name}"
        ))
        db.session.add(new_fd)
        db.session.commit()

        return jsonify({
            "msg": f"Investment with {offering.institution_name} locked!", 
            "end_time": finish_time.isoformat(),
            "new_balance": float(user.coin_balance)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "An error occurred while creating the deposit."}), 500

@finance_bp.route('/fd/withdraw', methods=['POST'])
@jwt_required()
def withdraw_fd():
    # Convert the identity string from the JWT back to an integer
    user_id = int(get_jwt_identity()) 
    
    data = request.get_json()
    fd_id = data.get('fd_id')
    
    # Use get_or_404 to handle cases where the FD doesn't exist
    fd = FixedDeposit.query.get_or_404(fd_id)
    
    # Now the integer comparison will work correctly
    if fd.user_id != user_id:
        return jsonify({"msg": "Unauthorized access to this deposit."}), 403

    now = datetime.utcnow()
    user = User.query.get(user_id)
    
    if now >= fd.end_time:
        # MATURED: Principal + Interest
        final_val = float(fd.principal) * (1 + float(fd.interest_rate))
        msg = f"Maturity reached! You earned ${final_val - float(fd.principal):.2f} in interest."
    else:
        # EARLY WITHDRAWAL: Lose all interest, return only principal
        final_val = float(fd.principal)
        msg = "Early withdrawal: Interest forfeited, principal returned."

    try:
        # Update user balance
        user.coin_balance += Decimal(str(final_val))
        
        # Log the transaction
        db.session.add(CoinTransaction(
            user_id=user_id, 
            amount=Decimal(str(final_val)), 
            activity_type=f"FD Withdrawal: {fd.institution.institution_name}"
        ))
        
        # Remove the deposit record
        db.session.delete(fd)
        db.session.commit()

        return jsonify({
            "msg": msg,
            "new_balance": float(user.coin_balance)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to process withdrawal.", "error": str(e)}), 500