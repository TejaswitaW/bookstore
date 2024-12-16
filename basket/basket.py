from decimal import Decimal

from store.models import Product

class Basket:
    """
    A base Basket class, providing some default behaviors that can be inherited or overrided,
    as necessary.
    """
    def __init__(self,request):
        self.session = request.session
        # print(type(self.session))
        basket = self.session.get('skey')
        if 'skey' not in self.session:
            basket = self.session['skey'] = {}
            #print("basket: ",basket)#Basket:  {9: {'price': '10.00', 'qty': 1}}
            # {'skey': {'9': {'price': '10.00', 'qty': 1}}}
        self.basket = basket

    def add(self,product,qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
            print("Basket: ",self.basket)
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    def delete(self,product):
        """
        Delete item from session data
        """
        # Receiving product_id in product
        # as its type is int ,but data that we store in session is string, so 
        # to make match we are doing typcasting
        
        product_id = str(product)
        # product_id = str(product)
        print("product_id in basket delete: ", product_id)
        print("Type product_id in basket delete: ", type(product_id))#int
        if product_id in self.basket:
            print("Self.basket product_id: ",product_id)
            del self.basket[product_id]
            self.save()

    def update(self, product, qty):
        """
        Update values in session data.
        """
        product_id = str(product)
        qty = qty

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
            print("Basket: ",self.basket)

        self.save()
        
    def save(self):
        self.session.modified = True

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database and return products.
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        # Copying an instance of session data.
        # It has everything that user has selected.
        # We will add some more data to basket data, for doing some calculations.
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item


    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())
    # Accessed as {{basket.get_total_price}} inside loop
    def get_total_price(self):
        # Getting data from original session i.e self.basket.
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())