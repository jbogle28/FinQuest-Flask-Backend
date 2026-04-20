# backend/app/routes/game_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.economy import CoinTransaction
from app.models.game import VocabularyTerm, GameHistory, CrosswordEntry, Crossword
from sqlalchemy import func
from urllib.parse import unquote

# Use one consistent blueprint for all game-related logic
game_bp = Blueprint('game', __name__)

# --- HANGMAN LOGIC ---

@game_bp.route('/hangman/start', methods=['GET'])
@jwt_required()
def start_hangman():
    user_id = get_jwt_identity()

    # 1. Get IDs of words this user already finished in Hangman
    # We look for 'Hangman' entries in GameHistory for this user
    already_solved_entries = GameHistory.query.filter_by(
        user_id=user_id, 
        game_type="Hangman"
    ).all()

    # Extract term_ids from the snapshot (assuming you store them there)
    # If you haven't started storing them yet, this list will be empty
    solved_ids = []
    for entry in already_solved_entries:
        if entry.quiz_snapshot and 'term_id' in entry.quiz_snapshot[0]:
            solved_ids.append(entry.quiz_snapshot[0]['term_id'])

    # 2. Find a random term that IS NOT in the solved_ids list
    term_entry = VocabularyTerm.query.filter(
        ~VocabularyTerm.term_id.in_(solved_ids)
    ).order_by(func.random()).first()
    
    # If they finished everything, reset or give a message
    if not term_entry:
        return jsonify({"msg": "Congratulations! You've mastered all terms!"}), 404

    return jsonify({
            "term_id": term_entry.term_id,
            "word": term_entry.term,  # Changed from display_word to word
            "definition": term_entry.definition,
            "category": term_entry.category
        }), 200

@game_bp.route('/hangman/guess', methods=['POST'])
@jwt_required()
def guess_letter():
    data = request.get_json()
    term_id = data.get('term_id')
    guess = data.get('guess').lower()
    
    term_entry = VocabularyTerm.query.get(term_id)
    word = term_entry.term.lower()
    
    if guess in word:
        indices = [i for i, letter in enumerate(word) if letter == guess]
        return jsonify({"correct": True, "indices": indices})
    else:
        return jsonify({"correct": False})

@game_bp.route('/hangman/result', methods=['POST'])
@jwt_required()
def hangman_result():
    user_id = get_jwt_identity()
    data = request.get_json()
    win = data.get('win')
    term_id = data.get('term_id') # Make sure frontend sends this
    
    if win:
        user = User.query.get(user_id)
        reward_amount = 50
        
        user.coin_balance += reward_amount
        user.xp_total += 20
        
        # Save history with the term_id so we don't show it again
        history = GameHistory(
            user_id=user_id, 
            game_type="Hangman", 
            score=100.0,
            quiz_snapshot=[{"term_id": term_id, "status": "completed"}]
        )
        
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            "msg": "Success!",
            "earned_xp": 20,
            "earned_coins": 50
        })
    
    return jsonify({"msg": "Try again!"})

# backend/app/routes/game_routes.py

@game_bp.route('/deduct-coins', methods=['POST'])
@jwt_required()
def deduct_coins():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Ensure amount is a number
    amount = data.get('amount', 50)
    activity = data.get('activity', 'Hint Purchase')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Use 0 as fallback for coin_balance
    current_balance = user.coin_balance or 0

    if current_balance < amount:
        return jsonify({"msg": "Insufficient coins"}), 400

    try:
        # 1. Update User Balance
        user.coin_balance = current_balance - amount
        
        # 2. Record Transaction (Matching your exact Model columns)
        new_transaction = CoinTransaction(
            user_id=user_id,
            amount=amount,          # Model has this
            activity_type=activity  # Model has this
            # created_at is handled by default=datetime.utcnow
        )
        
        db.session.add(new_transaction)
        db.session.commit()
        
        return jsonify({
            "msg": "Coins deducted", 
            "new_balance": float(user.coin_balance)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"DATABASE ERROR: {e}") 
        return jsonify({"msg": "Transaction failed", "error": str(e)}), 500
    


# --- CROSSWORD LOGIC ---
@game_bp.route('/crossword/<string:topic>', methods=['GET'])
@jwt_required()
def get_crossword(topic):
    # 1. Decode the URL to handle spaces properly (e.g., %20 -> " ")
    # This ensures "Budgeting Basics" matches what's in your seed.
    decoded_topic = unquote(topic).strip()
    
    # 2. Strict match for the topic
    puzzle = Crossword.query.filter_by(topic=decoded_topic).first()
    
    if not puzzle:
        # Debug print helps you see exactly what string failed in the terminal
        print(f"DEBUG: No puzzle found for exactly: '{decoded_topic}'")
        return jsonify({"msg": f"No crossword puzzle found for topic: {decoded_topic}"}), 404

    # 3. Structure the data for the React frontend
    # Fixed at 12x12 as requested
    puzzle_data = {
        "topic": puzzle.topic,
        "grid_size": 12, 
        "across": {},
        "down": {}
    }

    # 4. Map entries to the frontend structure
    for entry in puzzle.entries:
        entry_data = {
            "clue": entry.clue,
            "word": entry.word.upper(),
            "y": entry.y,
            "x": entry.x,
            "clue_number": entry.clue_number
        }
        
        # Ensure 'Across'/'Down' from DB are normalized to lowercase keys
        direction_key = entry.direction.lower()
        if direction_key in ["across", "down"]:
            puzzle_data[direction_key][str(entry.entry_id)] = entry_data

    return jsonify(puzzle_data), 200

@game_bp.route('/crossword/submit', methods=['POST'])
@jwt_required()
def submit_crossword():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    xp_reward = data.get('xp_reward', 100)
    
    # 1. FETCH USER FIRST (Outside the try block)
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # 2. Prepare the history object
    new_history = GameHistory(
        user_id=current_user_id,
        game_type='Crossword',
        score=float(xp_reward),
        quiz_snapshot=[{
            "topic": data.get('topic'),
            "completed": True,
            "time_taken": data.get('time_taken'),
            "grid_size": data.get('grid_size')
        }]
    )

    try:
        db.session.add(new_history)
        
        # 3. Update the user object that was already fetched
        user.coin_balance = (user.coin_balance or 0) + 50
        user.xp_total = (user.xp_total or 0) + xp_reward
        
        db.session.commit()
        
        return jsonify({
            "msg": "Progress saved!", 
            "xp": xp_reward,
            "coins_earned": 50
        }), 201
        
    except Exception as e:
        db.session.rollback()
        # It's better to print the error to your console for debugging
        print(f"Error saving crossword: {e}") 
        return jsonify({"msg": "Failed to save progress", "error": str(e)}), 500
    


# --- TIME CHALLENGE LOGIC ---

@game_bp.route('/time-challenge/start', methods=['GET'])
@jwt_required()
def start_time_challenge():
    """
    Fetches random vocabulary terms for the matching game.
    Query Param: ?count=4 (default)
    """
    # 1. Get the number of pairs requested (default to 4 for easy)
    count = request.args.get('count', default=4, type=int)
    
    # 2. Try to find terms specifically tagged for the Time Challenge first
    query = VocabularyTerm.query.filter_by(category='Time Challenge')
    
    # Fallback: If not enough 'Time Challenge' terms exist, get any terms
    if query.count() < count:
        query = VocabularyTerm.query

    # 3. Fetch random terms
    terms = query.order_by(func.random()).limit(count).all()

    # 4. Format for the frontend
    result = [{
        "term_id": t.term_id,
        "term": t.term,
        "definition": t.definition
    } for t in terms]

    return jsonify(result), 200

@game_bp.route('/time-challenge/submit', methods=['POST'])
@jwt_required()
def submit_time_challenge():
    """
    Handles rewards for completing the Time Challenge.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    xp_earned = data.get('xp', 25)
    coins_earned = data.get('coins', 10)
    difficulty = data.get('difficulty', 'easy')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    try:
        # Update user stats
        user.xp_total = (user.xp_total or 0) + xp_earned
        user.coin_balance = (user.coin_balance or 0) + coins_earned

        # Record in Game History
        history = GameHistory(
            user_id=user_id,
            game_type="Time Challenge",
            score=float(xp_earned),
            quiz_snapshot=[{
                "difficulty": difficulty,
                "pairs_matched": data.get('pairs_matched'),
                "time_remaining": data.get('time_remaining')
            }]
        )

        db.session.add(history)
        db.session.commit()

        return jsonify({
            "msg": "Challenge recorded!",
            "new_xp": user.xp_total,
            "new_balance": float(user.coin_balance)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Time Challenge Error: {e}")
        return jsonify({"msg": "Failed to save results"}), 500