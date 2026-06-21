from Seller import models
from django.shortcuts import get_object_or_404, render
from customers.models import signinm

def get_cart_count(request):
    if request.user.is_authenticated:
        customer = signinm.objects.filter(email=request.user.username).first()
        if customer:
            return customer.cart or 0
    return 0
def home(request):
    return render(request, 'home.html')
def products(request):
    products = models.sellm.objects.all()
    product=[]
    se=search(request)
    if se:
        products = models.sellm.objects.filter(category__icontains=se)
    return render(request, 'products.html', {'products': products, 'cart_count': get_cart_count(request)})
def sell(request):
    return render(request, 'sell.html')
def product(request,slug):
    product = get_object_or_404(models.sellm, slug=slug)
    return render(request, 'product.html', {'p': product, 'cart_count': get_cart_count(request)})
def search(request):
    return request.GET.get("search")
