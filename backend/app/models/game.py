# backend/app/models.py
from app import db


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(10), nullable=False)
    difficulty_level = db.Column(db.Integer, default=1)

class VocabularyTerm(db.Model):
    __tablename__ = 'vocabulary_terms'
    
    term_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))

class Crossword(db.Model):
    __tablename__ = 'crosswords'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(50), nullable=False) # e.g., "Budgeting"
    grid_size = db.Column(db.Integer, default=12) 
    difficulty = db.Column(db.Integer, default=1)
    
    # This links the puzzle to its specific entries
    entries = db.relationship('CrosswordEntry', backref='puzzle', lazy=True, cascade="all, delete-orphan")

class CrosswordEntry(db.Model):
    __tablename__ = 'crossword_entries'
    
    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # FOREIGN KEY: This links the entry to the specific Crossword ID
    crossword_id = db.Column(db.Integer, db.ForeignKey('crosswords.id'), nullable=False)
    
    word = db.Column(db.String(50), nullable=False)
    clue = db.Column(db.Text, nullable=False)
    
    # Grid positioning
    x = db.Column(db.Integer, nullable=False) # Column
    y = db.Column(db.Integer, nullable=False) # Row
    direction = db.Column(db.String(10), nullable=False) # 'across' or 'down'
    
    # This number appears in the corner of the cell (e.g., 1 Across, 1 Down)
    clue_number = db.Column(db.Integer, nullable=False)
    
class GameHistory(db.Model):
    __tablename__ = 'game_history'
    
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    game_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Numeric(10, 2), nullable=False)
    
    # For Crosswords, this can store: [{"topic": "...", "time_taken": 120}]
    quiz_snapshot = db.Column(db.JSON, nullable=True)
    completed_at = db.Column(db.DateTime, server_default=db.func.now())


class Scenario(db.Model):
    __tablename__ = 'scenarios'

    # Single Auto-incrementing ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), default='Stocks')
    prompt = db.Column(db.Text, nullable=False)
    
    option_a_title = db.Column(db.String(100), nullable=False)
    option_a_description = db.Column(db.Text, nullable=False)
    
    option_b_title = db.Column(db.String(100), nullable=False)
    option_b_description = db.Column(db.Text, nullable=False)
    
    option_c_title = db.Column(db.String(100), nullable=True)
    option_c_description = db.Column(db.Text, nullable=True)
    
    correct_option = db.Column(db.String(1), nullable=False) # 'A', 'B', or 'C'
    feedback = db.Column(db.JSON, nullable=False)
    lesson = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "prompt": self.prompt,
            "options": [
                {"id": "A", "title": self.option_a_title, "description": self.option_a_description},
                {"id": "B", "title": self.option_b_title, "description": self.option_b_description},
                *( [{"id": "C", "title": self.option_c_title, "description": self.option_c_description}] 
                   if self.option_c_title else [] )
            ],
            "correct_option": self.correct_option,
            "feedback": self.feedback,
            "lesson": self.lesson
        }