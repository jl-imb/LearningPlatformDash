from app.schemas import Module, Progress

modules_data = [
    Module(
        id="mod_1",
        title="Home Buying Basics",
        lessons=["What is a Mortgage?", "Down Payments 101", "Credit Scores"],
        total_coins=75,
        difficulty="Beginner"
    ),
    Module(
        id="mod_2",
        title="Home Inspections",
        lessons=["Types of Inspections", "Red Flags", "Negotiating Repairs"],
        total_coins=100,
        difficulty="Intermediate"
    ),
]

fake_users_db = {}
user_progress_db: list[Progress] = []
