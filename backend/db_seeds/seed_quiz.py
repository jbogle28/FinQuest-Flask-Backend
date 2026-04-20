from app import create_app, db
from app.models import QuizQuestion

app = create_app()

def seed_all_quizzes():
    all_questions = [
        # 1. Budgeting Basics (Level 1)
        {"text": "What is the best definition of a 'Budget'?", "topic": "Budgeting Basics", "diff": 1, "options": ["A way to stop spending", "A plan for spending and saving", "A list of things to buy", "A record of debt"], "correct": "B"},
        {"text": "The 50/30/20 rule suggests 50% of income goes to:", "topic": "Budgeting Basics", "diff": 1, "options": ["Wants", "Savings", "Needs", "Investments"], "correct": "C"},
        {"text": "Which is a 'Fixed Expense'?", "topic": "Budgeting Basics", "diff": 1, "options": ["Groceries", "Movie tickets", "Rent", "Gasoline"], "correct": "C"},
        {"text": "What is 'Net Income'?", "topic": "Budgeting Basics", "diff": 1, "options": ["Total salary before tax", "Take-home pay after tax", "Total savings", "Total debt"], "correct": "B"},
        {"text": "What is the first step in budgeting?", "topic": "Budgeting Basics", "diff": 1, "options": ["Investing", "Tracking income", "Buying a car", "Opening a credit card"], "correct": "B"},
        {"text": "Which is a 'Want'?", "topic": "Budgeting Basics", "diff": 1, "options": ["Electricity", "Water", "Designer shoes", "Rent"], "correct": "C"},
        {"text": "Tracking spending helps you:", "topic": "Budgeting Basics", "diff": 1, "options": ["Identify leaks", "Increase salary", "Get free money", "Avoid all taxes"], "correct": "A"},

        # 2. Emergency Funds (Level 1)
        {"text": "What is an Emergency Fund?", "topic": "Emergency Funds", "diff": 1, "options": ["Money for a vacation", "Money for unplanned expenses", "Money for retirement", "Money for a new TV"], "correct": "B"},
        {"text": "How many months of expenses is recommended for a basic fund?", "topic": "Emergency Funds", "diff": 1, "options": ["1 month", "3-6 months", "12 months", "1 week"], "correct": "B"},
        {"text": "Where should you keep an Emergency Fund?", "topic": "Emergency Funds", "diff": 1, "options": ["Under the mattress", "The stock market", "A liquid savings account", "In a long-term CD"], "correct": "C"},
        {"text": "Which is a valid reason to use your fund?", "topic": "Emergency Funds", "diff": 1, "options": ["New iPhone release", "Unexpected car repair", "A 50% off sale", "A friend's wedding gift"], "correct": "B"},
        {"text": "An emergency fund provides:", "topic": "Emergency Funds", "diff": 1, "options": ["High returns", "Financial security", "Tax breaks", "Debt increases"], "correct": "B"},
        {"text": "What is 'Liquidity'?", "topic": "Emergency Funds", "diff": 1, "options": ["Water in the bank", "How fast you can access cash", "Your total net worth", "The interest rate"], "correct": "B"},
        {"text": "Starting a fund is best done by:", "topic": "Emergency Funds", "diff": 1, "options": ["Waiting for a bonus", "Saving small amounts regularly", "Borrowing money", "Investing in Bitcoin"], "correct": "B"},

        # 3. Savings Accounts (Level 1)
        {"text": "What does APY stand for?", "topic": "Savings Accounts", "diff": 1, "options": ["Annual Percentage Yield", "Account Payment Yearly", "Actual Price Yield", "Annual Profit Yield"], "correct": "A"},
        {"text": "Which account usually pays interest?", "topic": "Savings Accounts", "diff": 1, "options": ["Checking Account", "Savings Account", "Credit Card", "Utility Account"], "correct": "B"},
        {"text": "What is the benefit of an Online Savings Account?", "topic": "Savings Accounts", "diff": 1, "options": ["Physical branches", "Often higher interest rates", "Free checks", "It's not real money"], "correct": "B"},
        {"text": "What is a 'Minimum Balance'?", "topic": "Savings Accounts", "diff": 1, "options": ["The most you can save", "The least you must keep to avoid fees", "The interest earned", "The bank's total cash"], "correct": "B"},
        {"text": "Why do people use savings accounts?", "topic": "Savings Accounts", "diff": 1, "options": ["To spend money fast", "To keep money safe and earn interest", "To play the stock market", "To avoid identity theft"], "correct": "B"},
        {"text": "Savings accounts are 'FDIC Insured'. What does this mean?", "topic": "Savings Accounts", "diff": 1, "options": ["Money is lost if bank fails", "Money is protected by government", "Money is invested in gold", "The bank is private"], "correct": "B"},
        {"text": "What is a 'Withdrawal limit'?", "topic": "Savings Accounts", "diff": 1, "options": ["Max money in account", "Restrictions on taking money out", "The interest cap", "The minimum age"], "correct": "B"},

        # 4. Debt Management (Level 1)
        {"text": "What is 'Principal' in a loan?", "topic": "Debt Management", "diff": 1, "options": ["The school head", "The original amount borrowed", "The interest paid", "The late fee"], "correct": "B"},
        {"text": "Which debt should you usually pay off first?", "topic": "Debt Management", "diff": 1, "options": ["Lowest interest", "Highest interest", "Newest debt", "Smallest debt"], "correct": "B"},
        {"text": "What is 'Interest'?", "topic": "Debt Management", "diff": 1, "options": ["The cost of borrowing money", "A free gift from the bank", "Your savings balance", "The tax on your salary"], "correct": "A"},
        {"text": "What happens if you only pay the 'Minimum' on a credit card?", "topic": "Debt Management", "diff": 1, "options": ["Debt is paid off fast", "You pay much more in interest over time", "Your interest stops", "The bank gives you a bonus"], "correct": "B"},
        {"text": "What is a 'Secured Loan'?", "topic": "Debt Management", "diff": 1, "options": ["A loan with no interest", "A loan backed by collateral (like a car)", "A loan from a friend", "A loan with no paperwork"], "correct": "B"},
        {"text": "A 'Late Fee' is applied when:", "topic": "Debt Management", "diff": 1, "options": ["You pay early", "You pay after the due date", "You pay the full balance", "You open the app"], "correct": "B"},
        {"text": "What does 'Refinancing' mean?", "topic": "Debt Management", "diff": 1, "options": ["Declaring bankruptcy", "Replacing a loan with a new one (lower rate)", "Ignoring the debt", "Paying in cash"], "correct": "B"},

        # 5. Credit Score 101 (Level 1)
        {"text": "What is a typical Credit Score range?", "topic": "Credit Score 101", "diff": 1, "options": ["0 - 100", "300 - 850", "500 - 1000", "1 - 10"], "correct": "B"},
        {"text": "What factor affects your score the most?", "topic": "Credit Score 101", "diff": 1, "options": ["Income", "Payment history", "Job title", "Age"], "correct": "B"},
        {"text": "Why does a good credit score matter?", "topic": "Credit Score 101", "diff": 1, "options": ["Higher interest rates", "Easier to get loans and better rates", "Free groceries", "Higher taxes"], "correct": "B"},
        {"text": "What is 'Credit Utilization'?", "topic": "Credit Score 101", "diff": 1, "options": ["Your total credit limit", "The percentage of available credit you use", "How many cards you have", "Your monthly income"], "correct": "B"},
        {"text": "Checking your own score 'Soft Inquiry' does what?", "topic": "Credit Score 101", "diff": 1, "options": ["Lowers it", "Doesn't affect it", "Increases it", "Deletes it"], "correct": "B"},
        {"text": "How often can you get a free credit report (US law)?", "topic": "Credit Score 101", "diff": 1, "options": ["Every day", "Once a year", "Every 10 years", "Never"], "correct": "B"},
        {"text": "A 'Hard Inquiry' usually happens when:", "topic": "Credit Score 101", "diff": 1, "options": ["You check your app", "You apply for a new loan/card", "You pay a bill", "You get a raise"], "correct": "B"},

        # 6. Stock Market Intro (Level 1)
        {"text": "What is a 'Stock'?", "topic": "Stock Market Intro", "diff": 1, "options": ["A loan to a company", "Partial ownership of a company", "A type of bank account", "Insurance policy"], "correct": "B"},
        {"text": "What is a 'Dividend'?", "topic": "Stock Market Intro", "diff": 1, "options": ["A stock market crash", "A portion of company profit paid to shareholders", "The price of one share", "A trading fee"], "correct": "B"},
        {"text": "What does 'Buy Low, Sell High' aim to do?", "topic": "Stock Market Intro", "diff": 1, "options": ["Lose money", "Make a profit", "Avoid taxes", "Diversify"], "correct": "B"},
        {"text": "What is an 'ETF'?", "topic": "Stock Market Intro", "diff": 1, "options": ["Electronic Transfer Fund", "Exchange Traded Fund", "Early Tax Fund", "Everyday Trading Firm"], "correct": "B"},
        {"text": "A 'Bull Market' means prices are:", "topic": "Stock Market Intro", "diff": 1, "options": ["Falling", "Rising", "Staying the same", "Crashing"], "correct": "B"},
        {"text": "A 'Bear Market' means prices are:", "topic": "Stock Market Intro", "diff": 1, "options": ["Rising", "Falling", "Stable", "At an all-time high"], "correct": "B"},
        {"text": "What is 'Diversification'?", "topic": "Stock Market Intro", "diff": 1, "options": ["Buying only one stock", "Spreading investments to reduce risk", "Selling all stocks", "Borrowing for stocks"], "correct": "B"},

        # 7. Compound Interest (Level 1)
        {"text": "What is Compound Interest?", "topic": "Compound Interest", "diff": 1, "options": ["Interest on the principal only", "Interest on the principal AND the accumulated interest", "A fee paid to the bank", "A flat tax rate"], "correct": "B"},
        {"text": "Compound interest is most powerful over:", "topic": "Compound Interest", "diff": 1, "options": ["1 week", "Long periods of time", "Overnight", "1 month"], "correct": "B"},
        {"text": "Einstein reportedly called compound interest the:", "topic": "Compound Interest", "diff": 1, "options": ["Greatest mistake", "Eighth wonder of the world", "Way to get poor", "Simple math"], "correct": "B"},
        {"text": "The 'Rule of 72' helps estimate:", "topic": "Compound Interest", "diff": 1, "options": ["Tax returns", "How long it takes to double your money", "Credit score", "Retirement age"], "correct": "B"},
        {"text": "Which frequency of compounding earns the most?", "topic": "Compound Interest", "diff": 1, "options": ["Yearly", "Daily", "Monthly", "Quarterly"], "correct": "B"},
        {"text": "If you start saving at age 20 vs age 40, you will likely have:", "topic": "Compound Interest", "diff": 1, "options": ["Less money", "Much more money", "The same amount", "Zero interest"], "correct": "B"},
        {"text": "Inflation does what to your purchasing power?", "topic": "Compound Interest", "diff": 1, "options": ["Increases it", "Decreases it over time", "Makes it double", "Has no effect"], "correct": "B"},

        # 8. Retirement Plans (Level 1)
        {"text": "What is a 401(k)?", "topic": "Retirement Plans", "diff": 1, "options": ["A tax-advantaged retirement plan through an employer", "A type of credit card", "A health insurance plan", "A government loan"], "correct": "A"},
        {"text": "What is an 'Employer Match'?", "topic": "Retirement Plans", "diff": 1, "options": ["Free money from your boss to your retirement account", "A dating app for coworkers", "A competitive salary", "A tax penalty"], "correct": "A"},
        {"text": "What is an IRA?", "topic": "Retirement Plans", "diff": 1, "options": ["Internal Revenue Agency", "Individual Retirement Account", "Investment Risk Asset", "Interest Rate Account"], "correct": "B"},
        {"text": "A 'Roth IRA' is funded with:", "topic": "Retirement Plans", "diff": 1, "options": ["Pre-tax dollars", "Post-tax dollars", "Company stock", "Borrowed money"], "correct": "B"},
        {"text": "Why should you start retirement saving early?", "topic": "Retirement Plans", "diff": 1, "options": ["To pay more taxes", "To take advantage of compound interest", "Because the law requires it", "To get a higher credit score"], "correct": "B"},
        {"text": "Social Security is meant to be your _____ source of income:", "topic": "Retirement Plans", "diff": 1, "options": ["Only", "Primary", "Supplemental", "Best"], "correct": "C"},
        {"text": "What is the 'Early Withdrawal Penalty'?", "topic": "Retirement Plans", "diff": 1, "options": ["A fee for taking money before a certain age", "A reward for saving", "A tax refund", "A bank bonus"], "correct": "A"},

        # 9. Tax Strategies (Level 1)
        {"text": "What is 'Taxable Income'?", "topic": "Tax Strategies", "diff": 1, "options": ["Total salary", "Income after deductions and exemptions", "Your bank balance", "Your credit limit"], "correct": "B"},
        {"text": "A 'Tax Deduction' does what?", "topic": "Tax Strategies", "diff": 1, "options": ["Increases your tax bill", "Reduces the amount of income subject to tax", "Is a direct refund", "Is a type of loan"], "correct": "B"},
        {"text": "What is a 'Tax Refund'?", "topic": "Tax Strategies", "diff": 1, "options": ["Interest from the IRS", "Money returned when you overpaid your taxes", "A gift from the president", "Your entire salary"], "correct": "B"},
        {"text": "The deadline for filing US taxes is usually:", "topic": "Tax Strategies", "diff": 1, "options": ["January 1", "April 15", "July 4", "December 31"], "correct": "B"},
        {"text": "What is a 'W-2' form?", "topic": "Tax Strategies", "diff": 1, "options": ["A job application", "A summary of your yearly earnings and taxes withheld", "A credit report", "A budget sheet"], "correct": "B"},
        {"text": "Which is a 'Direct Tax'?", "topic": "Tax Strategies", "diff": 1, "options": ["Sales tax", "Income tax", "VAT", "Import duty"], "correct": "B"},
        {"text": "Filing your taxes is:", "topic": "Tax Strategies", "diff": 1, "options": ["Optional", "Mandatory", "Only for the rich", "Once every 10 years"], "correct": "B"},

        # 10. Financial Freedom (Level 1)
        {"text": "What is Financial Freedom?", "topic": "Financial Freedom", "diff": 1, "options": ["Having $1 million", "Having enough passive income to cover expenses", "Winning the lottery", "Having no bank account"], "correct": "B"},
        {"text": "What is 'Passive Income'?", "topic": "Financial Freedom", "diff": 1, "options": ["Income from a 9-5 job", "Money earned with little to no daily effort", "A gift from parents", "Illegal money"], "correct": "B"},
        {"text": "What is 'Net Worth'?", "topic": "Financial Freedom", "diff": 1, "options": ["Your salary", "Assets minus Liabilities", "Cash in bank", "Value of your car"], "correct": "B"},
        {"text": "What is a 'Liability'?", "topic": "Financial Freedom", "diff": 1, "options": ["Something that puts money in your pocket", "Something that takes money out of your pocket (debt)", "A type of stock", "A savings goal"], "correct": "B"},
        {"text": "The FIRE movement stands for:", "topic": "Financial Freedom", "diff": 1, "options": ["Financial Independence, Retire Early", "Fast Income, Real Estate", "Fixed Interest, Really Easy", "Financial Integrity, Rural Energy"], "correct": "A"},
        {"text": "Which is an 'Asset'?", "topic": "Financial Freedom", "diff": 1, "options": ["Credit card debt", "A rental property", "Car loan", "Utility bill"], "correct": "B"},
        {"text": "Building multiple streams of income helps:", "topic": "Financial Freedom", "diff": 1, "options": ["Increase risk", "Reduce financial dependence on one job", "Pay more fees", "Slow down savings"], "correct": "B"},
    ]

    with app.app_context():
        print("Wiping existing questions...")
        db.session.query(QuizQuestion).delete()
        
        for q in all_questions:
            new_q = QuizQuestion(
                question_text=q['text'],
                topic=q['topic'],
                difficulty_level=q['diff'],
                option_a=q['options'][0],
                option_b=q['options'][1],
                option_c=q['options'][2],
                option_d=q['options'][3],
                correct_answer=q['correct']
            )
            db.session.add(new_q)
        
        db.session.commit()
        print(f"Success! Seeded {len(all_questions)} Level 1 questions across all categories.")

if __name__ == "__main__":
    seed_all_quizzes()