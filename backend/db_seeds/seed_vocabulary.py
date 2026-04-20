from app import create_app, db
from app.models import VocabularyTerm 

def seed_vocabulary():
    app = create_app()

    terms = [
        # --- CATEGORY: INVESTING (15 Terms) ---
        {"term": "Dividend", "definition": "A portion of a company's profit paid out to its shareholders.", "category": "Investing"},
        {"term": "Portfolio", "definition": "A collection of financial investments like stocks, bonds, and cash.", "category": "Investing"},
        {"term": "Bull Market", "definition": "A financial market condition where prices are rising or expected to rise.", "category": "Investing"},
        {"term": "Bear Market", "definition": "A market condition where prices are falling, encouraging selling.", "category": "Investing"},
        {"term": "Asset Allocation", "definition": "An investment strategy that aims to balance risk and reward by apportioning assets.", "category": "Investing"},
        {"term": "Blue Chip", "definition": "Stock in a well-established, financially sound company with a history of reliable growth.", "category": "Investing"},
        {"term": "Capital Gain", "definition": "The profit made from the sale of an asset or investment.", "category": "Investing"},
        {"term": "Diversification", "definition": "Spreading investments among different financial instruments to reduce risk.", "category": "Investing"},
        {"term": "Equity", "definition": "The value of shares issued by a company.", "category": "Investing"},
        {"term": "Index Fund", "definition": "A mutual fund designed to match or track the components of a financial market index.", "category": "Investing"},
        {"term": "Liquidity", "definition": "The ease with which an asset can be converted into cash without affecting its price.", "category": "Investing"},
        {"term": "Mutual Fund", "definition": "An investment program funded by shareholders that trades in diversified holdings.", "category": "Investing"},
        {"term": "Speculation", "definition": "Investment in stocks or property in the hope of gain but with the risk of loss.", "category": "Investing"},
        {"term": "Volatility", "definition": "The degree of variation of a trading price series over time.", "category": "Investing"},
        {"term": "Yield", "definition": "The income return on an investment, such as interest or dividends received.", "category": "Investing"},

        # --- CATEGORY: BUDGETING (15 Terms) ---
        {"term": "Emergency Fund", "definition": "Money set aside to cover unexpected financial surprises or expenses.", "category": "Budgeting"},
        {"term": "Fixed Expense", "definition": "An expense that does not change from month to month, such as rent.", "category": "Budgeting"},
        {"term": "Net Worth", "definition": "The total value of everything you own minus all your debts.", "category": "Budgeting"},
        {"term": "Inflation", "definition": "The rate at which the general level of prices for goods and services is rising.", "category": "Budgeting"},
        {"term": "Sinking Fund", "definition": "Money saved over time for a specific future purchase or expense.", "category": "Budgeting"},
        {"term": "Variable Expense", "definition": "Costs that change based on your usage, like groceries or utilities.", "category": "Budgeting"},
        {"term": "Gross Income", "definition": "Total earnings before any taxes or deductions are taken out.", "category": "Budgeting"},
        {"term": "Net Income", "definition": "The amount of money you actually take home after all deductions.", "category": "Budgeting"},
        {"term": "Deficit", "definition": "When your spending exceeds your income over a specific period.", "category": "Budgeting"},
        {"term": "Surplus", "definition": "The amount of money remaining when income exceeds expenses.", "category": "Budgeting"},
        {"term": "Discretionary", "definition": "Spending on non-essential items like entertainment or dining out.", "category": "Budgeting"},
        {"term": "Cash Flow", "definition": "The total amount of money being transferred into and out of a household.", "category": "Budgeting"},
        {"term": "Zero Based Budget", "definition": "A method where every dollar of income is assigned a specific purpose.", "category": "Budgeting"},
        {"term": "Needs", "definition": "Essential expenses required for survival, such as housing and food.", "category": "Budgeting"},
        {"term": "Wants", "definition": "Expenses that improve quality of life but are not necessary for survival.", "category": "Budgeting"},

        # --- CATEGORY: CREDIT & DEBT (10 Terms) ---
        {"term": "Interest Rate", "definition": "The amount charged by a lender to a borrower for the use of assets.", "category": "Credit"},
        {"term": "Credit Score", "definition": "A numerical expression representing a person's creditworthiness.", "category": "Credit"},
        {"term": "Collateral", "definition": "An asset that a lender accepts as security for a loan.", "category": "Credit"},
        {"term": "Principal", "definition": "The original sum of money borrowed or put into an investment.", "category": "Credit"},
        {"term": "Amortization", "definition": "The process of gradually paying off a debt over a set period.", "category": "Credit"},
        {"term": "APR", "definition": "Annual Percentage Rate; the total cost of borrowing per year.", "category": "Credit"},
        {"term": "Bankruptcy", "definition": "A legal proceeding involving a person or business that is unable to repay debts.", "category": "Credit"},
        {"term": "Default", "definition": "Failure to fulfill an obligation, especially to repay a loan.", "category": "Credit"},
        {"term": "Grace Period", "definition": "The time during which you can pay your bill without incurring interest.", "category": "Credit"},
        {"term": "Usury", "definition": "The illegal action or practice of lending money at unreasonably high interest rates.", "category": "Credit"},

        # --- CATEGORY: BANKING & ECONOMICS (10 Terms) ---
        {"term": "Compound Interest", "definition": "Interest calculated on the principal and accumulated interest.", "category": "Banking"},
        {"term": "Fiscal Year", "definition": "A one-year period used for financial reporting and budgeting.", "category": "Banking"},
        {"term": "Recession", "definition": "A period of temporary economic decline with reduced industrial activity.", "category": "Economics"},
        {"term": "GDP", "definition": "Gross Domestic Product; the total value of goods produced in a country.", "category": "Economics"},
        {"term": "Overdraft", "definition": "A deficit in a bank account caused by drawing more money than the account holds.", "category": "Banking"},
        {"term": "Direct Deposit", "definition": "The electronic transfer of a payment directly into a recipient's bank account.", "category": "Banking"},
        {"term": "Central Bank", "definition": "A national bank that provides financial services to the government and banking system.", "category": "Banking"},
        {"term": "Hyperinflation", "definition": "Extremely rapid or out-of-control inflation.", "category": "Economics"},
        {"term": "Fiat Money", "definition": "Currency that is not backed by a physical commodity like gold.", "category": "Economics"},
        {"term": "Monopoly", "definition": "The exclusive possession or control of the supply or trade in a commodity.", "category": "Economics"},

        # --- CATEGORY: TIME CHALLENGE (50 Terms) ---
        # Short, fast-paced terms for the 60-second game
        {"term": "Debit", "definition": "Money taken out of an account.", "category": "Time Challenge"},
        {"term": "Credit", "definition": "Money added to an account.", "category": "Time Challenge"},
        {"term": "Loan", "definition": "Money borrowed that must be repaid.", "category": "Time Challenge"},
        {"term": "Tax", "definition": "Mandatory fee paid to the government.", "category": "Time Challenge"},
        {"term": "Bond", "definition": "A fixed income instrument like a loan.", "category": "Time Challenge"},
        {"term": "Stock", "definition": "A share in the ownership of a company.", "category": "Time Challenge"},
        {"term": "Cash", "definition": "Money in the form of notes or coins.", "category": "Time Challenge"},
        {"term": "Bank", "definition": "Financial institution for saving and lending.", "category": "Time Challenge"},
        {"term": "Goal", "definition": "A target for saving or spending.", "category": "Time Challenge"},
        {"term": "Save", "definition": "Setting money aside for the future.", "category": "Time Challenge"},
        {"term": "Plan", "definition": "A detailed proposal for your finances.", "category": "Time Challenge"},
        {"term": "Risk", "definition": "The chance of loss in an investment.", "category": "Time Challenge"},
        {"term": "Loss", "definition": "When an investment decreases in value.", "category": "Time Challenge"},
        {"term": "Gain", "definition": "When an investment increases in value.", "category": "Time Challenge"},
        {"term": "ATM", "definition": "Automated machine for bank transactions.", "category": "Time Challenge"},
        {"term": "Card", "definition": "Plastic tool used for payments.", "category": "Time Challenge"},
        {"term": "Fee", "definition": "A payment made for a service.", "category": "Time Challenge"},
        {"term": "Debt", "definition": "Something, typically money, that is owed.", "category": "Time Challenge"},
        {"term": "Bill", "definition": "A statement of money owed for goods.", "category": "Time Challenge"},
        {"term": "Rent", "definition": "Regular payment for use of property.", "category": "Time Challenge"},
        {"term": "Wages", "definition": "Money paid for work or services.", "category": "Time Challenge"},
        {"term": "Sale", "definition": "Exchange of goods for money.", "category": "Time Challenge"},
        {"term": "Coin", "definition": "Small, flat, round piece of metal money.", "category": "Time Challenge"},
        {"term": "Buck", "definition": "Informal term for a dollar.", "category": "Time Challenge"},
        {"term": "Cent", "definition": "A monetary unit equal to 1/100 of a dollar.", "category": "Time Challenge"},
        {"term": "Check", "definition": "A written order to pay a sum of money.", "category": "Time Challenge"},
        {"term": "Vault", "definition": "A secure room for storing valuables.", "category": "Time Challenge"},
        {"term": "Price", "definition": "The amount of money expected for a product.", "category": "Time Challenge"},
        {"term": "Cost", "definition": "The amount required to be paid for something.", "category": "Time Challenge"},
        {"term": "Earn", "definition": "To receive money as payment for work.", "category": "Time Challenge"},
        {"term": "Spend", "definition": "To pay out money in buying goods.", "category": "Time Challenge"},
        {"term": "Wallet", "definition": "A pocket-sized case for holding money.", "category": "Time Challenge"},
        {"term": "Budget", "definition": "An estimate of income and expenditure.", "category": "Time Challenge"},
        {"term": "Audit", "definition": "Official inspection of financial accounts.", "category": "Time Challenge"},
        {"term": "Market", "definition": "Place where stocks or goods are traded.", "category": "Time Challenge"},
        {"term": "Broker", "definition": "Person who buys/sells for others.", "category": "Time Challenge"},
        {"term": "Shares", "definition": "Equal parts into which capital is divided.", "category": "Time Challenge"},
        {"term": "Option", "definition": "Contract giving the right to buy/sell.", "category": "Time Challenge"},
        {"term": "Ticker", "definition": "Device that displays stock prices.", "category": "Time Challenge"},
        {"term": "Wealth", "definition": "Abundance of valuable possessions.", "category": "Time Challenge"},
        {"term": "Grant", "definition": "Non-repayable fund given by a party.", "category": "Time Challenge"},
        {"term": "Lender", "definition": "Organization that loans money.", "category": "Time Challenge"},
        {"term": "Escrow", "definition": "Account held by a third party.", "category": "Time Challenge"},
        {"term": "Tariff", "definition": "Tax on imported or exported goods.", "category": "Time Challenge"},
        {"term": "Quota", "definition": "A fixed share of something that is allowed.", "category": "Time Challenge"},
        {"term": "Trust", "definition": "Legal arrangement for holding property.", "category": "Time Challenge"},
        {"term": "Legacy", "definition": "Money or property left in a will.", "category": "Time Challenge"},
        {"term": "Stable", "definition": "Not likely to change or fail.", "category": "Time Challenge"},
        {"term": "Growth", "definition": "Increase in value over time.", "category": "Time Challenge"},
        {"term": "Bull", "definition": "Optimistic about price increases.", "category": "Time Challenge"}
    ]

    with app.app_context():
        # Clear existing terms if needed
        db.session.query(VocabularyTerm).delete()
        
        for item in terms:
            exists = VocabularyTerm.query.filter_by(term=item['term']).first()
            if not exists:
                new_term = VocabularyTerm(
                    term=item['term'],
                    definition=item['definition'],
                    category=item['category']
                )
                db.session.add(new_term)
        
        db.session.commit()
        print(f"Successfully seeded {len(terms)} vocabulary terms!")

if __name__ == "__main__":
    seed_vocabulary()