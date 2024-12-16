from .basket import Basket


def basket(request):
    # accessing data in the given basket and making available to all pages
    return {'basket':Basket(request)}