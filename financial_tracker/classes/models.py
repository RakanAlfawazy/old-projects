class User:
    def __init__(self, username: str) -> None:
        self.username: str = username

class Transaction:
    def __init__(self, user_id: int, amount: float, category: str, date: str, t_type: str) -> None:
        self.user_id: int = user_id
        self.amount: float = amount
        self.category: str = category
        self.date: str = date
        self.type: str = t_type
