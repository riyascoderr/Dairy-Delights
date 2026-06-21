from . import views
from django.urls import path
app_name='seller'
urlpatterns = [
    path('sign-in/', views.signin, name='signin'),
    path('log-in/', views.loginn, name='loginn'),
    path('log-out/', views.logouti, name='logouti'),
    path('data/', views.seller, name='data'),
]
