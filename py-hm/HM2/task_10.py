class BankError(Exception):
    def __init__(self, message: str, balance: int, amount: int, *args):
        super().__init__(message, *args)
        self.balance = balance
        self.amount = amount

class InvalidAmountError(BankError):
    pass

class InsufficientFundsError(BankError):
    pass

class AccountBlockedError(BankError):
    pass

def withdraw(balance: int, amount: int):
    if amount <= 0:
        raise InvalidAmountError("Можно снимать только положительную сумму", balance, amount)
    if balance < amount:
        raise InsufficientFundsError("Недостаточно средств", balance, amount)
    return balance - amount

try:
    withdraw(200, 0)
except InvalidAmountError as e:
    print("Некорректная сумма:", e)
    print("Баланс:", e.balance)
    print("Сумма снятия:", e.amount)
except InsufficientFundsError as e:
    print("Ошибка счёта:", e)
    print("Баланс:", e.balance)
    print("Сумма снятия:", e.amount)
except BankError as e:
    print("Другая ошибка банковского счёта:", e)