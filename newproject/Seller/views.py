from django.shortcuts import render,redirect
from .forms import sellf, signinf
from .models import sellm, signins
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.text import slugify
from django.utils.text import slugify
from .forms import sellf
from customers import models

@login_required(login_url='home')
def seller(request):
    if request.method == 'POST':
        form = sellf(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.seller = request.user  # ✅ assign seller before saving
            instance.slug = slugify(request.POST.get('name'))
            instance.save()
            return redirect('products')
        else:
            print(form.errors)  # shows missing fields
    else:
        form = sellf()
    return render(request, 'sell.html', {'form': form})
def signin(request):
    if request.method=="POST":
        name=request.POST.get('seller_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        location=request.POST.get('location')
        gst_number=request.POST.get('gst_number')
        password=request.POST.get('password')
        try:
            User.objects.get(username=email)
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('sell')
            else:
                return HttpResponse("Invalid credentials")
        except User.DoesNotExist:
            user=User.objects.create_user(username=email,password=password)
            signins.objects.create(seller_name=name,email=email,phone=phone,location=location,gst_number=gst_number)
            models.signinm.objects.create(name=name,email=email,phone=phone,address=location)
            login(request, user)
            return redirect('sell')
    return render(request,'home.html',{'form': signinf()})
def loginn(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('sell')
        else:
            return HttpResponse("Invalid credentials")
    return render(request,'home.html',{'form': signinf()})
def logouti(request):
    logout(request)
    return redirect('home')
