from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bank(models.Model):
    Branch_Name=models.CharField(max_length=100)
    Code=models.CharField(max_length=100)
    Address=models.TextField(max_length=200)



class USER_Role(models.Model):
    choices=[('debit','DEBIT'),('credit','CREDIT')]
    Role=models.CharField(choices)
    User_id=models.ForeignKey(User,on_delete=models.DO_NOTHING)


class User_Account(models.Model):
    Account_number=models.CharField(max_length=14)
    User_id=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    Current_Balance=models.DecimalField(decimal_places=1,max_digits=100, default=0.0)
    is_active=models.BooleanField(default=True)
    Created_date=models.DateTimeField(auto_now=True)


class Transcations(models.Model):
    Date=models.DateTimeField(auto_now=True)
    Amount=models.DecimalField(decimal_places=1,max_digits=10)
    choices=[('withdraw','WITHDRAW'),('deposit','DEPOSIT'),('transfer','TRANSFER')]
    Type=models.CharField(choices)
    From_Acc=models.ForeignKey(User_Account,related_name='related',on_delete=models.DO_NOTHING)
    To_Acc=models.ForeignKey(User_Account,related_name='num',on_delete=models.DO_NOTHING)
    Remaning_Balance=models.CharField(max_length=10)
    User_id = models.ForeignKey(User,null=True ,on_delete=models.DO_NOTHING)