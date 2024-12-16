from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .basket import Basket
from store.models import Product

def basket_summary(request):
    basket = Basket(request)
    return render(request,'basket/summary.html',{'basket':basket})

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product,id=product_id)
        basket.add(product=product,qty=product_qty)
        basketqty = basket.__len__()
        response = JsonResponse({'qty':basketqty})  
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        print("Basket delete: ",basket)# <basket.basket.Basket object at 0x000001AD3F442B50>
        product_id = int(request.POST.get('productid'))
        # Just check the keys in the session i.e product_id
        basket.delete(product=product_id)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))

        print("Product id in upate: ",product_id)
        print("Product qauntity in update: ",product_qty)

        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()

        print("Baskettotal in update: ",baskettotal)
        print("Basket qty: ",basketqty)
        # No need to send product id send back to FE
        response = JsonResponse({'qty':basketqty, 'subtotal':baskettotal})

        return response

