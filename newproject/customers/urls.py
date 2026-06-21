from . import views
from django.urls import path
app_name='customers'
urlpatterns = [
    path('sign-in/', views.signin, name='signin'),
    path('log-in/', views.loginn, name='loginn'),
    path('log-out/', views.logouti, name='logouti'),
    path('gen-ai/', views.genai, name='genai'),
    path('buy/', views.buy, name='buy'),
    path("cart/",views.cart,name="cart")
]
