from django.shortcuts import render,redirect
from .forms import signinf,loginf,buyf
from .models import signinm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from Seller import models
def signin(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        password=request.POST.get('password')
        try:
            User.objects.get(username=email)
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('products')
            else:
                return HttpResponse("Invalid credentials")
        except User.DoesNotExist:
            user=User.objects.create_user(username=email,password=password)
            signinm.objects.create(name=name,email=email,phone=phone,address=address)
            login(request, user)
            return redirect('products')
    return render(request,'home.html',{'form': signinf()})
def loginn(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('products')
        else:
            return HttpResponse("Invalid credentials")
    return render(request,'home.html',{'form': loginf()})
def logouti(request):
    logout(request)
    return redirect('home')
def genai(request):
    if request.method=="POST":
        question=request.POST.get("aiQuestion")
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        price=request.POST.get("price")
        size=request.POST.get("size")
        product_type=request.POST.get("type")
        ingredients=request.POST.get("ingredients")
        packaging=request.POST.get("packaging")
        shelf_life=request.POST.get("shelf_life")
        delivery_slot=request.POST.get("delivery_slot")
        description=request.POST.get("description")

        if question:
            import os
            import google.generativeai as genai
            from dotenv import load_dotenv

            load_dotenv()
            api_key = os.getenv("Google_API_Key")
            prompt = f"""
            You are a helpful dairy product assistant.
            Answer the customer question using the product details.

            Product name: {product_name}
            Brand: {brand}
            Price: Rs. {price}
            Size: {size}
            Type: {product_type}
            Ingredients: {ingredients}
            Packaging: {packaging}
            Shelf life: {shelf_life}
            Delivery slot: {delivery_slot}
            Description: {description}

            Customer question: {question}
            """

            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                return HttpResponse(response.text)
            except Exception as error:
                return HttpResponse("GenAI error: " + str(error))
    return redirect('products')
def buy(request):
    if request.method=="POST":
        form=buyf(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
        return HttpResponse("Invalid buy form data")
    return redirect('products')

def get_customer(request):
    return signinm.objects.get(email=request.user.username)

def add_item(items, sku):
    if sku:
        items.append(sku)
    return items

def delete_item(items, sku):
    if sku in items:
        items.remove(sku)
    return items

def save_cart(customer, items):
    customer.items = items
    customer.cart = len(items)
    customer.save(update_fields=["items", "cart"])

def get_cart_products(customer):
    products = []
    for sku in customer.items:
        product = models.sellm.objects.filter(sku=sku).first()
        if product:
            products.append(product)
    return products

def get_cart_total(products):
    subtotal = sum(product.price for product in products)
    delivery = 0
    deposit = 0

    if products:
        delivery = 25
        deposit = 10

    total = subtotal + delivery + deposit

    return subtotal, delivery, deposit, total

def cart(request):
    if not request.user.is_authenticated:
        return redirect('home')

    customer = get_customer(request)

    if request.method == "POST":
        sku = request.POST.get("sku")
        action = request.POST.get("action")
        next_page = request.POST.get("next")
        items = list(customer.items or [])

        if action == "delete":
            items = delete_item(items, sku)
        else:
            items = add_item(items, sku)

        save_cart(customer, items)
        if next_page == "products":
            return redirect("products")
        return redirect("customers:cart")

    items = get_cart_products(customer)
    subtotal, delivery, deposit, total = get_cart_total(items)

    return render(request, "cart.html", {
        "items": items,
        "cart_count": len(items),
        "subtotal": subtotal,
        "delivery": delivery,
        "deposit": deposit,
        "total": total,
    })


        
