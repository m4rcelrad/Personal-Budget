from datetime import datetime

class Expense:
    def __init__(self, name, category, amount, date=None, description="", essentiality="essential"):
        self.name = name
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.essentiality = essentiality  # nowy atrybut

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Expense(**data)


class Income:
    def __init__(self, name, category, amount, date=None, description=""):
        self.name = name
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Income(**data)