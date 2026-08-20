"""
URL configuration for Application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from BANK.views import Deposit,Withdraw,Transfer,View_Transaction,Register,Login,Home,logout_view
from BANK.views import Check_Balance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Deposit',Deposit,name='Deposit-page'),
    path('Withdraw',Withdraw,name="withdraw"),
    path('Transfer',Transfer,name="Transfer"),
    path('view_Transcation',View_Transaction),
    path('CheckBalance', Check_Balance),
    path('',Register),
    path('login',Login,name="login-page"),
    path('Home-page',Home,name="Home"),
    path('logout',logout_view,name="logout")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
