from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse

import secrets
from .models import User_Account,Transcations
from django.contrib.auth import login
from django.contrib.auth import logout
import json
from decimal import Decimal
# Create your views here.
@csrf_exempt
def Deposit(request):
    if not request.user.is_authenticated:
            return redirect("login-page")
    user_account=User_Account.objects.get(User_id=request.user)
    
    if request.method=='POST':
        amount=request.POST.get('Amount')
        print(amount)
        messages.success(
            request,f"Successfully {amount} credited to your account!"
        )
        user= request.user
        account=User_Account.objects.get(User_id=user)
        new_transcations=Transcations.objects.create(
            Amount=Decimal(amount),
            Type="deposit",
            From_Acc=account,
            To_Acc=account,
            User_id=user
        )
        new_transcations.save()
        account.Current_Balance += Decimal(amount)
        account.save()
        return redirect("Deposit-page")
    account={
       'account_number': user_account.Account_number,

       
    }
    print(account)
    return render(request,'Deposit.html',context=account)

    

def logout_view(request):
    logout(request)
    return redirect("login-page")

@csrf_exempt
def Withdraw(request):
    if  not request.user.is_authenticated:

        return redirect("login-page")
    user=request.user
    user_Account=User_Account.objects.get(User_id=user) 
    if request.method=='GET':
        data={
            'account_number': user_Account.Account_number
        }
        return render(request,'Withdraw.html',context=data)
    elif request.method=='POST':
        withdraw_amount=request.POST.get("withdraw_amount")
        
              
        if Decimal(withdraw_amount) > user_Account.Current_Balance:
            return render(request,'Withdraw.html',context={'error':'insufficient Balance'})
        
        new_transcations=Transcations.objects.create(
                    Amount=Decimal(withdraw_amount),
                    Type="withdraw",
                    From_Acc=user_Account,
                    To_Acc=user_Account,
                    Remaning_Balance=withdraw_amount,
                    User_id=user
                    
                )
        
        new_transcations.save()
        print(new_transcations)
        user_Account.Current_Balance -= Decimal(withdraw_amount)
        user_Account.save()
        print(user_Account)
        return redirect("withdraw")

        
    

@csrf_exempt
def Transfer(request):
    if not request.user.is_authenticated:
        return redirect("login-page")
    if request.method=='GET':
        user=request.user
        user_account= User_Account.objects.get(User_id=user)
        data={
            'account_number': user_account.Account_number
        }
        return render(request,'Transfer.html',context=data)
    elif request.method=='POST':
        transfer=request.POST.get("transfer_amount")
        to_acc=request.POST.get("To_account")
        to_account = User_Account.objects.filter(Account_number=to_acc)
        user=request.user
        user_account= User_Account.objects.get(User_id=user)
        if len(to_account)<1:
            return render(request,'Transfer.html',context={'error':'Account does not Exist'})
        own_account=User_Account.objects.filter(
            User_id=request.user,
            Account_number=to_acc
        ).exists()
        if own_account:
            return render(request,'Transfer.html', context={'error':'You cannot Transfer into your own Account'})
      
        to_account = to_account.first()
        print(to_account)
        new_transcations=Transcations.objects.create(
            Amount=transfer,
            Type='transfer',
            From_Acc=user_account,
            To_Acc=to_account, 
            Remaning_Balance=transfer,
            User_id=user
            
        )
        new_transcations.save()
        user_account.Current_Balance -= Decimal(transfer)
        user_account.save()
        print(user_account)
        transcation=Transcations.objects.create(
            Amount=transfer,
            Type='transfer',
            From_Acc=to_account,
            To_Acc=user_account,     
        )
        transcation.save()
        print(transcation)
        to_account.Current_Balance += Decimal(transfer)
        to_account.save()
        print(to_account)
        return redirect("Transfer")





def Check_Balance(request):
    if not request.user.is_authenticated:
        return redirect("login-page")
    if request.method =="GET":
        
        user_account=User_Account.objects.filter(User_id=request.user)
        return render(request,'Check_Balance.html', context={"user_accounts":user_account})
      


@csrf_exempt
def Login(request):
    if request.method=='GET':
        return render(request,'login.html')
    if request.method=='POST':
        data=request.POST
        username=data.get('email')
        password=data.get('password')
        user = User.objects.filter(username=username)

        if len(user) < 1:
            return render(request, 'login.html',context={'error':'invalid username'})

        user = user[0]
        check=user.check_password(password)

        if not check:
            return render(request,'login.html',context={'error':'invalid password'})
        login(request, user)
        return redirect("Home")




@csrf_exempt
def View_Transaction(request):
    if not request.user.is_authenticated:
        return redirect("login-page")
    if request.method == 'GET':
        user=request.user
        transcation=Transcations.objects.filter(
            User_id=user
            
        )
        details={
            'transfer':transcation
        }
        print(transcation.values(),"-----------------")
        
        return render(request,'view-transaction.html',context=details)
        
    


@csrf_exempt
def Register(request):
    if request.method=='GET':
        return render(request,'Register.html')
    if request.method=='POST':
        data=request.POST
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        username=data.get('email')
        password=data.get('password')
        confirm_password=data.get('confirm_password')
    if len(firstname)<=1:
        return render(request,'Register.html',context={'error':'firstname cannot be one alphabet'})
    if User.objects.filter(username=username).exists():
        return render(request,"Register.html",context={"error":"Email already existis"})
    if (password!=confirm_password):
        return render(request,'Register.html',context={'error':'Password  should be same as confirm Password'})
    number="".join(str(secrets.randbelow(10))for i in range(14))
    new_user=User.objects.create(username=username,password=password) 
    new_user.set_password(password)
    new_user.save()
    print(number)
    account=User_Account.objects.create(User_id=new_user,Account_number=number)
    account.save()
    print(account)
    return   redirect("login-page") 

 
def Home(request):
    if not request.user.is_authenticated:
        return redirect("login-page")
    user=request.user
    user_account=User_Account.objects.filter(User_id=user)

    if len(user_account)<1:
        return redirect('login-page')
        
    user_account=user_account[0]
    account = {
        'account_number': user_account.Account_number,
        'username':user_account.User_id.username,
        'Current_Balance':user_account.Current_Balance
    }
    print(account)
    return render(request,'Homepage.html',context=account)

@csrf_exempt    
def check_acc_number(request):
    if request.method =='POST':
        data = json.loads(request.body.decode("utf-8"))
        acc_no = data.get('accountnumber')
        user=request.user
        # filter accounts with account number
        user_account = User_Account.objects.filter(
            Account_number=acc_no,
            
          
        ).first()
        print("Found account:",user_account)
        # check at least account is filtered
        if user_account:
            username=user_account.User_id.username
            print(username)
            return JsonResponse({"success": True,"username":username,"accountnumber":user_account.Account_number})
   



       

