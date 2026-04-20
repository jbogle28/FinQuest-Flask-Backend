# seed_crosswords.py
from app import create_app, db
from app.models.game import Crossword, CrosswordEntry

def seed_data():
    app = create_app()
    with app.app_context():
        print("Clearing old crossword data...")
        db.session.query(CrosswordEntry).delete()
        db.session.query(Crossword).delete()
        db.session.commit()

        puzzles = [
            {
                "topic": "Budgeting Basics",
                "difficulty": 1,
                "grid_size": 12,
                "entries": [
                    {"clue": "Money owed to another party.", "word": "DEBT", "x": 0, "y": 0, "direction": "Down", "clue_number": 1},
                    {"clue": "A plan for spending and saving.", "word": "BUDGET", "x": 0, "y": 2, "direction": "Across", "clue_number": 2},
                    {"clue": "Money spent on goods or services.", "word": "EXPENSE", "x": 4, "y": 2, "direction": "Down", "clue_number": 3},
                    {"clue": "Money set aside for future use.", "word": "SAVINGS", "x": 4, "y": 7, "direction": "Across", "clue_number": 4},
                    {"clue": "Money received on a regular basis.", "word": "INCOME", "x": 8, "y": 6, "direction": "Down", "clue_number": 5}
                ]
            },
            {
                "topic": "Banking & Accounts",
                "difficulty": 1,
                "grid_size": 12,
                "entries": [
                    # ACROSS CLUES
                    {"word": "DEPOSIT", "clue": "To put money into a bank account.", "x": 0, "y": 0, "direction": "across", "clue_number": 1},
                    {"word": "BALANCE", "clue": "The total amount of money in an account.", "x": 0, "y": 2, "direction": "across", "clue_number": 3},
                    {"word": "CHECKING", "clue": "An account for everyday spending and bills.", "x": 3, "y": 5, "direction": "across", "clue_number": 5},
                    {"word": "ATM", "clue": "Automated Teller Machine for cash withdrawals.", "x": 2, "y": 10, "direction": "across", "clue_number": 6},
                    
                    # DOWN CLUES
                    {"word": "INCOME", "clue": "Money received on a regular basis for work or investments.", "x": 5, "y": 0, "direction": "down", "clue_number": 2},
                    {"word": "ACCOUNT", "clue": "A record of financial transactions for a client.", "x": 3, "y": 4, "direction": "down", "clue_number": 4}
                ]
            },
            # {
            #     "topic": "Investment 101 - Advanced",
            #     "difficulty": 1,
            #     "grid_size": 13, # Accommodating the 13 columns
            #     "entries": [
            #         # ACROSS CLUES
            #         {"word": "RISK", "clue": "The possibility of loss on an investment.", "x": 2, "y": 3, "direction": "across", "clue_number": 2},
            #         {"word": "BONDS", "clue": "Fixed-income securities representing a loan.", "x": 0, "y": 7, "direction": "across", "clue_number": 3},
            #         {"word": "ASSETS", "clue": "Items of value owned by a person or company.", "x": 3, "y": 12, "direction": "across", "clue_number": 5},
                    
            #         # DOWN CLUES
            #         {"word": "DIVIDEND", "clue": "A distribution of a portion of a company's earnings.", "x": 3, "y": 0, "direction": "down", "clue_number": 1},
            #         {"word": "STOCKS", "clue": "Ownership shares in a corporation.", "x": 4, "y": 7, "direction": "down", "clue_number": 4}
            #     ]
            # },
            {
                "topic": "Credit & Debt",
                "difficulty": 1,
                "grid_size": 12,
                "entries": [
                    # ACROSS CLUES
                    {"word": "LOAN", "clue": "Borrowed money that is expected to be paid back with interest.", "x": 2, "y": 1, "direction": "across", "clue_number": 2},
                    {"word": "SCORE", "clue": "A numerical expression based on a level analysis of a person's credit files.", "x": 0, "y": 3, "direction": "across", "clue_number": 3},
                    {"word": "LIMIT", "clue": "The maximum amount of credit a financial institution extends to a client.", "x": 0, "y": 7, "direction": "across", "clue_number": 5},
                    
                    # DOWN CLUES
                    {"word": "LATE", "clue": "A fee charged when a payment is not made by the due date.", "x": 4, "y": 0, "direction": "down", "clue_number": 1},
                    {"word": "CREDIT", "clue": "The ability of a customer to obtain goods or services before payment.", "x": 1, "y": 2, "direction": "down", "clue_number": 4}
                ]
            },
            {
                "topic": "Retirement & Future",
                "difficulty": 1,
                "grid_size": 12,
                "entries": [
                    # ACROSS CLUES
                    {"word": "ESTATE", "clue": "All the money and property owned by a person.", "x": 2, "y": 2, "direction": "across", "clue_number": 2},
                    {"word": "WILL", "clue": "A legal document that expresses a person's final wishes.", "x": 1, "y": 5, "direction": "across", "clue_number": 3},
                    {"word": "ANNUITY", "clue": "A fixed sum of money paid to someone each year, typically for the rest of their life.", "x": 0, "y": 7, "direction": "across", "clue_number": 4},
                    
                    # DOWN CLUES
                    {"word": "PENSION", "clue": "A fund into which a sum of money is added during an employee's employment years.", "x": 2, "y": 1, "direction": "down", "clue_number": 1},
                    {"word": "ROTH", "clue": "An individual retirement account (IRA) that offers tax-free growth and withdrawals.", "x": 6, "y": 0, "direction": "down", "clue_number": 5}
                ]
            },
            {
                "topic": "Taxes & Freedom",
                "difficulty": 1,
                "grid_size": 12,
                "entries": [
                    # ACROSS CLUES
                    {"word": "REFUND", "clue": "Money back from the government when you overpay taxes.", "x": 0, "y": 1, "direction": "across", "clue_number": 1},
                    {"word": "AUDIT", "clue": "An official inspection of an individual's or organization's accounts.", "x": 2, "y": 5, "direction": "across", "clue_number": 5},
                    
                    # DOWN CLUES
                    {"word": "FISCAL", "clue": "Relating to government revenue, especially taxes.", "x": 2, "y": 1, "direction": "down", "clue_number": 2},
                    {"word": "NET", "clue": "The amount of income left after all taxes and deductions.", "x": 4, "y": 1, "direction": "down", "clue_number": 3},
                    {"word": "EXEMPT", "clue": "Free from an obligation, such as not having to pay certain taxes.", "x": 6, "y": 0, "direction": "down", "clue_number": 4}
                ]
            }
        ]

        for p_data in puzzles:
            new_p = Crossword(
                topic=p_data["topic"], 
                difficulty=p_data["difficulty"],
                grid_size=p_data["grid_size"]
            )
            db.session.add(new_p)
            db.session.flush()

            for e in p_data["entries"]:
                entry = CrosswordEntry(
                    crossword_id=new_p.id,
                    word=e["word"].upper(),
                    clue=e["clue"],
                    x=e["x"],
                    y=e["y"],
                    direction=e["direction"],
                    clue_number=e["clue_number"]
                )
                db.session.add(entry)
            print(f"Added '{p_data['topic']}' puzzle.")

        try:
            db.session.commit()
            print("Successfully seeded all 6 puzzles.")
        except Exception as err:
            db.session.rollback()
            print(f"Commit failed: {err}")

if __name__ == '__main__':
    seed_data()