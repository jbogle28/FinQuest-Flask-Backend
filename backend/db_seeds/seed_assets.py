from app import create_app, db
from app.models import QuizQuestion

app = create_app()

def seed_all_quizzes():
    all_questions = [
        # 1. Budgeting Basics
        {"text": "What is budgeting?", "topic": "Budgeting Basics", "diff": 1, "options": ["Tracking past spending", "A plan for future spending", "Avoiding expenses", "Saving only"], "correct": "B"},
        {"text": "According to the 50/30/20 rule, 50% of income goes to:", "topic": "Budgeting Basics", "diff": 1, "options": ["Wants", "Needs", "Savings", "Investments"], "correct": "B"},
        {"text": "Which of the following is a NEED?", "topic": "Budgeting Basics", "diff": 1, "options": ["Netflix", "Dining out", "Rent", "Gaming"], "correct": "C"},
        {"text": "What should you NOT do when budgeting?", "topic": "Budgeting Basics", "diff": 1, "options": ["Track expenses", "Spend less than you earn", "Use credit for everything", "Stick to plan"], "correct": "C"},
        {"text": "What is net income?", "topic": "Budgeting Basics", "diff": 1, "options": ["Salary before tax", "Take-home pay", "Savings", "Debt"], "correct": "B"},
        {"text": "Which is a WANT?", "topic": "Budgeting Basics", "diff": 1, "options": ["Electricity", "Water", "Designer shoes", "Rent"], "correct": "C"},
        {"text": "What is the first step in financial planning?", "topic": "Budgeting Basics", "diff": 1, "options": ["Get a job", "Determine your goals and needs", "Buy a house", "Save money"], "correct": "B"},

        # 2. Emergency Funds
        {"text": "What is the purpose of an emergency fund?", "topic": "Emergency Funds", "diff": 1, "options": ["Luxury purchases", "Unexpected expenses", "Investing", "Travel"], "correct": "B"},
        {"text": "Recommended emergency fund size is:", "topic": "Emergency Funds", "diff": 1, "options": ["1 week", "1 month", "3-6 months", "1 year"], "correct": "C"},
        {"text": "Where should emergency funds be kept?", "topic": "Emergency Funds", "diff": 1, "options": ["Stocks", "Savings account", "Crypto", "Real estate"], "correct": "B"},
        {"text": "Which is a valid emergency?", "topic": "Emergency Funds", "diff": 1, "options": ["New phone", "Car repair", "Vacation", "Shoes"], "correct": "B"},
        {"text": "Liquidity means:", "topic": "Emergency Funds", "diff": 1, "options": ["Water", "Easy access to money", "High returns", "Tax savings"], "correct": "B"},
        {"text": "Best way to build an emergency fund:", "topic": "Emergency Funds", "diff": 1, "options": ["Wait for bonus", "Save regularly", "Borrow money", "Invest risky"], "correct": "B"},
        {"text": "Emergency funds provide:", "topic": "Emergency Funds", "diff": 1, "options": ["High profits", "Security", "Debt", "Taxes"], "correct": "B"},

        # 3. Savings Accounts
        {"text": "What does 'Pay Yourself First' mean?", "topic": "Savings Accounts", "diff": 1, "options": ["Save after spending", "Save before spending", "Save yearly", "Save bonuses"], "correct": "B"},
        {"text": "Best example of Pay Yourself First:", "topic": "Savings Accounts", "diff": 1, "options": ["Save leftovers", "Auto transfer on payday", "Save once", "Save gifts"], "correct": "B"},
        {"text": "If inflation is higher than interest:", "topic": "Savings Accounts", "diff": 1, "options": ["Money grows", "No change", "Purchasing power decreases", "Money doubles"], "correct": "C"},
        {"text": "If inflation is higher than your savings interest rate, your money will:", "topic": "Savings Accounts", "diff": 1, "options": ["Increase in value", "Stay the same", "Lose purchasing power", "Double"], "correct": "C"},
        {"text": "APY stands for:", "topic": "Savings Accounts", "diff": 1, "options": ["Annual Percentage Yield", "Account Pay Yearly", "Actual Profit Yield", "Annual Payment"], "correct": "A"},
        {"text": "Savings accounts are mainly used to:", "topic": "Savings Accounts", "diff": 1, "options": ["Spend fast", "Keep money safe", "Invest stocks", "Avoid taxes"], "correct": "B"},
        {"text": "When developing a savings plan, what is the best approach?", "topic": "Savings Accounts", "diff": 1, "options": ["Wait until older", "Pay yourself first", "Only invest risky", "Avoid saving"], "correct": "B"},

        # 4. Debt Management
        {"text": "Best strategy to pay off multiple debts?", "topic": "Debt Management", "diff": 1, "options": ["Ignore debt", "Debt Snowball", "Borrow more", "Wait"], "correct": "B"},
        {"text": "A loan is:", "topic": "Debt Management", "diff": 1, "options": ["Free money", "Borrowed money with interest", "Savings", "Income"], "correct": "B"},
        {"text": "Interest is:", "topic": "Debt Management", "diff": 1, "options": ["Free money", "Cost of borrowing", "Savings", "Tax"], "correct": "B"},
        {"text": "If you don’t pay debt, it:", "topic": "Debt Management", "diff": 1, "options": ["Shrinks", "Grows", "Stops", "Disappears"], "correct": "B"},
        {"text": "15-year mortgage vs 30-year:", "topic": "Debt Management", "diff": 1, "options": ["Lower payments", "Higher payments, less interest", "More interest", "Same"], "correct": "B"},
        {"text": "A credit card is a form of borrowing money.", "topic": "Debt Management", "diff": 1, "options": ["True", "False", "Sometimes", "Don't know"], "correct": "A"},
        {"text": "At high interest rates (around 20%), debt will double in:", "topic": "Debt Management", "diff": 1, "options": ["Less than 2 years", "2–4 years", "5–9 years", "10+ years"], "correct": "B"},

        # 5. Credit Score 101
        {"text": "Credit score range is:", "topic": "Credit Score 101", "diff": 1, "options": ["0-100", "300-850", "500-1000", "1-10"], "correct": "B"},
        {"text": "Most important factor:", "topic": "Credit Score 101", "diff": 1, "options": ["Income", "Payment history", "Age", "Job"], "correct": "B"},
        {"text": "Good credit helps:", "topic": "Credit Score 101", "diff": 1, "options": ["Higher rates", "Better loan approval", "More tax", "Free money"], "correct": "B"},
        {"text": "Credit utilization is:", "topic": "Credit Score 101", "diff": 1, "options": ["Income", "Credit used %", "Savings", "Debt"], "correct": "B"},
        {"text": "Soft inquiry:", "topic": "Credit Score 101", "diff": 1, "options": ["Hurts score", "No effect", "Deletes score", "Raises score"], "correct": "B"},
        {"text": "Hard inquiry happens when:", "topic": "Credit Score 101", "diff": 1, "options": ["Check app", "Apply for credit", "Pay bill", "Save money"], "correct": "B"},
        {"text": "Good credit leads to:", "topic": "Credit Score 101", "diff": 1, "options": ["Higher interest", "Lower interest", "More debt", "Less income"], "correct": "B"},

        # 6. Stock Market Intro
        {"text": "Diversification reduces:", "topic": "Stock Market Intro", "diff": 1, "options": ["Profit", "Risk", "Taxes", "Debt"], "correct": "B"},
        {"text": "Dividend is:", "topic": "Stock Market Intro", "diff": 1, "options": ["Loss", "Profit paid to investors", "Loan", "Tax"], "correct": "B"},
        {"text": "Stock means:", "topic": "Stock Market Intro", "diff": 1, "options": ["Loan", "Ownership", "Tax", "Savings"], "correct": "B"},
        {"text": "Bull market:", "topic": "Stock Market Intro", "diff": 1, "options": ["Falling", "Rising", "Flat", "Crash"], "correct": "B"},
        {"text": "Bear market:", "topic": "Stock Market Intro", "diff": 1, "options": ["Rising", "Falling", "Stable", "Peak"], "correct": "B"},
        {"text": "ETF is:", "topic": "Stock Market Intro", "diff": 1, "options": ["Loan", "Fund traded on exchange", "Tax", "Debt"], "correct": "B"},
        {"text": "Buy low sell high aims to:", "topic": "Stock Market Intro", "diff": 1, "options": ["Lose money", "Profit", "Tax", "Diversify"], "correct": "B"},

        # 7. Compound Interest
        {"text": "Compound interest is:", "topic": "Compound Interest", "diff": 1, "options": ["Interest on original", "Interest on interest", "Tax", "Fee"], "correct": "B"},
        {"text": "Starting early gives:", "topic": "Compound Interest", "diff": 1, "options": ["Less money", "More growth", "Same money", "No interest"], "correct": "B"},
        {"text": "Rule of 72 estimates:", "topic": "Compound Interest", "diff": 1, "options": ["Tax", "Doubling time", "Salary", "Debt"], "correct": "B"},
        {"text": "Compounding works best over:", "topic": "Compound Interest", "diff": 1, "options": ["Short time", "Long time", "Instant", "Daily only"], "correct": "B"},
        {"text": "Higher compounding frequency:", "topic": "Compound Interest", "diff": 1, "options": ["Less growth", "More growth", "No effect", "Loss"], "correct": "B"},
        {"text": "Inflation does:", "topic": "Compound Interest", "diff": 1, "options": ["Increase value", "Reduce value", "No change", "Double value"], "correct": "B"},
        {"text": "Why is it beneficial to start investing at a young age?", "topic": "Compound Interest", "diff": 1, "options": ["Lower taxes", "More time for compounding", "Less risk", "More salary"], "correct": "B"},

        # 8. Retirement Plans
        {"text": "Start early because:", "topic": "Retirement Plans", "diff": 1, "options": ["More tax", "More compounding", "Less income", "No reason"], "correct": "B"},
        {"text": "401(k) is:", "topic": "Retirement Plans", "diff": 1, "options": ["Loan", "Retirement plan", "Tax", "Insurance"], "correct": "B"},
        {"text": "Employer match is:", "topic": "Retirement Plans", "diff": 1, "options": ["Loan", "Free contribution", "Tax", "Salary"], "correct": "B"},
        {"text": "IRA means:", "topic": "Retirement Plans", "diff": 1, "options": ["Tax", "Retirement account", "Loan", "Savings"], "correct": "B"},
        {"text": "Early withdrawal penalty:", "topic": "Retirement Plans", "diff": 1, "options": ["Reward", "Fee", "Bonus", "Tax refund"], "correct": "B"},
        {"text": "Roth IRA uses:", "topic": "Retirement Plans", "diff": 1, "options": ["Pre-tax", "Post-tax", "Loan", "Stock"], "correct": "B"},
        {"text": "Social Security is:", "topic": "Retirement Plans", "diff": 1, "options": ["Primary income", "Supplemental income", "Loan", "Tax"], "correct": "B"},

        # 9. Tax Strategies
        {"text": "Taxable income is:", "topic": "Tax Strategies", "diff": 1, "options": ["Total income", "Income after deductions", "Savings", "Debt"], "correct": "B"},
        {"text": "Tax deduction:", "topic": "Tax Strategies", "diff": 1, "options": ["Increase tax", "Reduce taxable income", "Loan", "Income"], "correct": "B"},
        {"text": "Tax refund:", "topic": "Tax Strategies", "diff": 1, "options": ["Loan", "Returned overpaid tax", "Salary", "Debt"], "correct": "B"},
        {"text": "Filing taxes is:", "topic": "Tax Strategies", "diff": 1, "options": ["Optional", "Mandatory", "Rare", "Illegal"], "correct": "B"},
        {"text": "Direct tax:", "topic": "Tax Strategies", "diff": 1, "options": ["Sales tax", "Income tax", "Import duty", "VAT"], "correct": "B"},
        {"text": "W-2 form shows:", "topic": "Tax Strategies", "diff": 1, "options": ["Credit score", "Income and tax paid", "Savings", "Debt"], "correct": "B"},
        {"text": "Tax deadline (US):", "topic": "Tax Strategies", "diff": 1, "options": ["Jan 1", "April 15", "July 4", "Dec 31"], "correct": "B"},

        # 10. Financial Freedom
        {"text": "Financial freedom means:", "topic": "Financial Freedom", "diff": 1, "options": ["Millionaire", "Passive income covers expenses", "No job", "No bank"], "correct": "B"},
        {"text": "Passive income is:", "topic": "Financial Freedom", "diff": 1, "options": ["Job income", "Earn with little effort", "Gift", "Loan"], "correct": "B"},
        {"text": "Net worth is:", "topic": "Financial Freedom", "diff": 1, "options": ["Income", "Assets minus liabilities", "Savings", "Debt"], "correct": "B"},
        {"text": "Liability is:", "topic": "Financial Freedom", "diff": 1, "options": ["Asset", "Debt", "Income", "Savings"], "correct": "B"},
        {"text": "Asset is:", "topic": "Financial Freedom", "diff": 1, "options": ["Debt", "Something that makes money", "Bill", "Loan"], "correct": "B"},
        {"text": "FIRE means:", "topic": "Financial Freedom", "diff": 1, "options": ["Fast Income", "Financial Independence Retire Early", "Tax plan", "Loan"], "correct": "B"},
        {"text": "Multiple income streams:", "topic": "Financial Freedom", "diff": 1, "options": ["Increase risk", "Reduce dependence on one job", "Lose money", "Pay tax"], "correct": "B"},
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
        print(f"Success! Seeded {len(all_questions)} questions across all categories.")

if __name__ == "__main__":
    seed_all_quizzes()