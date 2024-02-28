from django.shortcuts import render, redirect
from .tasks import order_created
# Create your views here.
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order = order,
                                         product = item['product'],
                                         price = item['price'],
                                         quantity = item['quantity'])
            
            #cleare cart
            cart.clear()
            #Создание асинхронного задания
            order_created.delay(order.id)
            #создание заказа в сеансе
            request.session['order_id'] = order.id
            #перенаправить к платежу
            return redirect(reverse('payment:process'))
    
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', 
                  {'cart': cart, 'form': form})