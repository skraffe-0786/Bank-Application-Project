from django.urls import path
from . import views
from .views import TransferView

urlpatterns = [
    path('accounts/', views.accounts,name='accounts'),
    path('accounts/<int:id>/', views.accounts, name='account-details'),
    path('forgotpassword',views.Forgotpassword, name='forgot'),
    path('transfer/',TransferView.as_view())
]