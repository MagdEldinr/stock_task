from retry import retry

from .models import Stock, User, Transaction
from .exceptions import BoundsException

def check_transaction_bounds(stock: Stock, upper_bound: int, lower_bound: int):
    if stock.price < lower_bound or stock.price > upper_bound:
        raise BoundsException
    return

@retry(BoundsException, delay=3, tries=5)
def buy_stock(user: User, stock: Stock, upper_bound: int, lower_bound: int, total: int):
    import ipdb; ipdb.set_trace()
    check_transaction_bounds(stock, upper_bound, lower_bound)    
    user.funds -= stock.price * total
    stock.availability -= total
    stock.save()
    user.save()
    Transaction.objects.create(stock=stock, user=user, action_type="buy")

@retry(BoundsException, delay=5, tries=5)
def sell_stock(user: User, stock: Stock, upper_bound: int, lower_bound: int, total: int):
    check_transaction_bounds(stock, upper_bound, lower_bound)    
    user.funds += stock.price * total
    stock.availability += total
    stock.save()
    user.save()
    Transaction.objects.create(stock=stock, user=user, action_type="sell")
