from app import db
from .user import User, Role, completed_scenarios
from .economy import CoinTransaction, Investment
from .game import QuizQuestion, VocabularyTerm, GameHistory, CrosswordEntry, Crossword, Scenario
from .cosmetics import Cosmetic, UserCosmetic
from .market import AvailableStock, AvailableBond, UserPortfolio, FixedDeposit