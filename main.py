import math


class Category:

    def __init__(self, category: str):
        self.category = category
        self.ledger = []
        self._balance = 0

    def deposit(self, amount: float, description: str = ""):
        transaction = {"amount": amount, "description": description}
        self._balance += amount
        self.ledger.append(transaction)

    def withdraw(self, amount: float, description: str = ""):
        if not self.check_funds(amount):
            return False
        transaction = {"amount": -amount, "description": description}
        self._balance -= amount
        self.ledger.append(transaction)
        return True

    def transfer(self, amount: float, categoryObj):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {categoryObj.category}")
        categoryObj.deposit(amount, f"Transfer from {self.category}")
        return True

    def get_balance(self):
        return self._balance

    def check_funds(self, amount: float):
        if self._balance < amount:
            return False
        return True

    def centerDisplay(self, category: str):
        lenCategory = len(category)
        remaining = 30 - lenCategory
        half = remaining // 2
        return f"{'*' * half}{category}{'*' * half}\n"

    def __str__(self):
        response = ""
        response += self.centerDisplay(self.category)
        for transactions in self.ledger:
            response += f"{transactions['description'][:23]:<23}{transactions['amount']:>7.2f}\n"
        response += f"Total: {self._balance}"
        return response


def createChart(categories: dict):
    noOfCategories = len(categories)
    percentvalues = categories.values()
    percentages = [f"{str(i):>3}" for i in range(0, 101, 10)]
    response = "Percentage spent by category\n"
    filled_index = [0]*noOfCategories
    for i in range(10, -1, -1):
        line = f"{percentages[i]}| "
        current_percent = i*10
        ind = [k for k, val in enumerate(percentvalues) if val == current_percent]
        for index in range(noOfCategories):
            if index in ind or filled_index[index]:
                filled_index[index] = 1
                line += f"o{' '*2}"
            else:
                line += f"{' '*3}"
        response += f"{line}\n"
    response += f"{' '*4}-{'-'*3*noOfCategories}\n"
    categoryKeys = categories.keys()
    maxLength = max([len(i) for i in categoryKeys])
    categoryList = []
    for key in categoryKeys:
        result = list(f"{key:<{maxLength}}")
        categoryList.append(result)
    result = list(zip(*categoryList))
    for keys in range(len(result)):
        response += f"{' ' * 5}"
        response += f"{' ' * 2}".join(result[keys])
        response += '  '
        if keys != len(result) - 1:
            response += '\n'
    return response


def create_spend_chart(categories: list[Category]):
    category_total = {}
    for category in categories:
        for transaction in category.ledger:
            if transaction['amount'] < 0:
                category_total[category.category] = category_total.get(category.category, 0) + (-transaction['amount'])
    total = sum(category_total.values())
    for category in category_total:
        percent = math.floor((category_total[category]*100) / total) // 10
        category_total[category] = int(percent) * 10
    return createChart(category_total)


