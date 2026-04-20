from app import create_app
from app.extensions import db
from app.models.game import Scenario

app = create_app()

stock_scenarios = [
    {
        "id": 1,
        "category": "Fundamental Analysis",
        "prompt": "Which company appears safer based on the information provided?",
        "option_a_title": "CoreSoft Technologies",
        "option_a_description": "• Operating for over 20 years\n• Holds about 20% market share\n• Reports consistent profits\n• Experienced CEO",
        "option_b_title": "FlashWave Media",
        "option_b_description": "• Founded 2 years ago\n• Crowded streaming market\n• Not yet profitable\n• CEO controversy affecting brand",
        "correct_option": "A",
        "feedback": {
            "A": "You chose CoreSoft. Strong fundamentals and product expansion led to growth. You made a profit.",
            "B": "FlashWave struggled with competition and controversy. The stock dropped and you lost money."
        },
        "lesson": "Established companies with profits and strong leadership are usually safer than new companies in crowded industries."
    },
    {
        "id": 2,
        "category": "Risk Management",
        "prompt": "Which stock is the safer investment?",
        "option_a_title": "SkyMint AI",
        "option_a_description": "• Fast-growing startup\n• Relies on investor hype\n• Product launch delayed due to technical issues",
        "option_b_title": "Northline Manufacturing",
        "option_b_description": "• Operating 25 years\n• Stable earnings\n• Recently secured long-term contract",
        "correct_option": "B",
        "feedback": {
            "A": "SkyMint AI lost investor confidence after delays. Stock dropped.",
            "B": "Northline Manufacturing remained stable and grew steadily. You made a profit."
        },
        "lesson": "Stable earnings and contracts are safer than hype-driven growth."
    },
    {
        "id": 3,
        "category": "Portfolio Strategy",
        "prompt": "Which investment decision is the safest?",
        "option_a_title": "VoltEdge Devices",
        "option_a_description": "• New electronics company\n• High debt\n• Possible recall risk",
        "option_b_title": "Metro Business Systems",
        "option_b_description": "• 18 years in business\n• Multiple revenue streams\n• Recently expanded into new markets",
        "option_c_title": "BalancedTech Fund",
        "option_c_description": "• Invests in multiple companies\n• Moderate returns\n• Lower volatility",
        "correct_option": "B",
        "feedback": {
            "A": "VoltEdge had a product recall and stock crashed. You lost money.",
            "B": "Metro Business Systems grew steadily. You made a profit.",
            "C": "BalancedTech Fund stayed stable. You neither gained nor lost much."
        },
        "lesson": "Diversification reduces risk, but strong fundamentals still outperform unstable companies."
    },
    {
        "id": 4,
        "category": "Market Sentiment",
        "prompt": "Which company is safer?",
        "option_a_title": "PrimeAxis Retail Tech",
        "option_a_description": "• 15+ years in business\n• Stable earnings\n• New partnership announced",
        "option_b_title": "QuickCart Online",
        "option_b_description": "• New company\n• Low profit margins\n• Major investor recently sold shares",
        "correct_option": "A",
        "feedback": {
            "A": "PrimeAxis expanded successfully. Stock increased.",
            "B": "QuickCart lost investor confidence after large sell-off. Stock dropped."
        },
        "lesson": "Investor sell-offs and weak margins are warning signs."
    },
    {
        "id": 5,
        "category": "Revenue Models",
        "prompt": "Which investment is safer?",
        "option_a_title": "TrendLoop Entertainment",
        "option_a_description": "• New entertainment app\n• Depends on trends\n• Weak earnings report",
        "option_b_title": "EverPeak Software",
        "option_b_description": "• 22 years in business\n• Subscription revenue\n• Stable profits",
        "correct_option": "B",
        "feedback": {
            "A": "TrendLoop failed to generate stable income. Stock dropped.",
            "B": "EverPeak grew consistently. You made a profit."
        },
        "lesson": "Recurring revenue is more stable than trend-based income."
    },
    {
        "id": 6,
        "category": "Economic Moats",
        "prompt": "Which investment would you choose?",
        "option_a_title": "IslandVision Media",
        "option_a_description": "• Inconsistent profits\n• Depends on ad revenue\n• CEO controversy ongoing",
        "option_b_title": "Harbor Utilities Group",
        "option_b_description": "• 30+ years in business\n• Stable demand\n• Approved expansion project",
        "option_c_title": "IncomeBond Fund",
        "option_c_description": "• Low risk investment\n• Stable but low returns\n• Government-backed",
        "correct_option": "B",
        "feedback": {
            "A": "IslandVision struggled with competition and controversy. Stock fell.",
            "B": "Harbor Utilities performed well. You made money.",
            "C": "IncomeBond stayed stable. No major gains or losses."
        },
        "lesson": "Stable industries with predictable demand are safer than competitive markets."
    },
    {
        "id": 7,
        "category": "Asset Diversification",
        "prompt": "Which company is the safer choice?",
        "option_a_title": "BioPeak Therapeutics",
        "option_a_description": "• Depends on one drug\n• Awaiting approval\n• Testing delays announced",
        "option_b_title": "HealthAxis Care",
        "option_b_description": "• 19 years in business\n• Multiple products\n• Strong quarterly earnings",
        "correct_option": "B",
        "feedback": {
            "A": "BioPeak faced delays and uncertainty. Stock dropped.",
            "B": "HealthAxis performed strongly. You gained money."
        },
        "lesson": "Dependence on one product increases risk."
    },
    {
        "id": 8,
        "category": "Policy & Regulation",
        "prompt": "Which investment is the safest?",
        "option_a_title": "SolarRise Energy",
        "option_a_description": "• High debt\n• Depends on subsidies\n• Policy changes may affect growth",
        "option_b_title": "NorthBridge Holdings",
        "option_b_description": "• 28 years in business\n• Diversified income\n• Dividend increased recently",
        "option_c_title": "Stable Income Fund",
        "option_c_description": "• Low risk/Low return\n• Diversified bonds\n• Stable growth",
        "correct_option": "B",
        "feedback": {
            "A": "SolarRise struggled due to policy changes. Stock dropped.",
            "B": "NorthBridge grew steadily. You made money.",
            "C": "Stable Income Fund remained flat. Minimal gains."
        },
        "lesson": "Diversification and profitability reduce risk."
    },
    {
        "id": 9,
        "category": "Business Ethics",
        "prompt": "Which company appears safer?",
        "option_a_title": "CloudAxis Systems",
        "option_a_description": "• Subscription revenue\n• Stable profits\n• Experienced leadership",
        "option_b_title": "PlayForge Interactive",
        "option_b_description": "• Relies on game releases\n• Mixed early reviews\n• Risk of failure",
        "correct_option": "A",
        "feedback": {
            "A": "CloudAxis grew steadily. You made a profit.",
            "B": "PlayForge's game disappointed. Stock dropped."
        },
        "lesson": "Recurring revenue is more reliable than hit-based income."
    },
    {
        "id": 10,
        "category": "Crisis Management",
        "prompt": "Which investment is safer?",
        "option_a_title": "DriveNova Motors",
        "option_a_description": "• New EV company\n• Not profitable\n• Massive product recall announced",
        "option_b_title": "Atlas Mobility Group",
        "option_b_description": "• 25+ years in business\n• Stable profits\n• Strong quarterly sales reported",
        "correct_option": "B",
        "feedback": {
            "A": "DriveNova suffered losses after recall. Stock crashed.",
            "B": "Atlas performed strongly. You gained money."
        },
        "lesson": "Recalls and debt are major risk signals."
    }
]

def seed_database():
    with app.app_context():
        # Clear existing to prevent duplicates during testing
        db.session.query(Scenario).delete() 
        
        for s in stock_scenarios:
            new_scenario = Scenario(
                id=s['id'],
                category=s['category'],
                prompt=s['prompt'],
                option_a_title=s['option_a_title'],
                option_a_description=s['option_a_description'],
                option_b_title=s['option_b_title'],
                option_b_description=s['option_b_description'],
                option_c_title=s.get('option_c_title'),
                option_c_description=s.get('option_c_description'),
                correct_option=s['correct_option'],
                feedback=s['feedback'],
                lesson=s['lesson']
            )
            db.session.add(new_scenario)
        
        db.session.commit()
        print(f"Successfully seeded {len(stock_scenarios)} scenarios with categories!")

if __name__ == "__main__":
    seed_database()