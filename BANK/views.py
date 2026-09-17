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
import re

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AccountSerializer
from  rest_framework import status
from .import views 

import random
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
        user = User.objects.filter(username=username).first()

        if not user:
            return render(request, 'login.html',context={'error':'invalid username'})
        if not user.check_password(password):
            return render(request,'login.html', context={"error":"Invalid User or Password"})

      


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
    errors=[]
    if len(password)<8 :
        errors.append("Password  must be  at least 8 characters")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least  one Uppercase Letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one Lowercase Letter .")
    if not re.search(r"[0-9]",password):
        errors.append("Password must  contain  at least one number .")
    if not re.search(r"[@#$!*%&]",password):
        errors.append("password must contain at least one special  character such as @,#,$,!,*,&")
    if errors:
        return  render(request, 'Register.html',context={"errors":errors})

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
   


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def accounts(request, id=None):

    # GET
    if request.method == 'GET':
        account = User_Account.objects.all()
        serializer = AccountSerializer(account, many=True)
        return Response(serializer.data)

    # POST
    elif request.method == 'POST':
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PUT / PATCH
    elif request.method in ['PUT', 'PATCH']:

        # Find the account first
        try:
            account = User_Account.objects.get(id=id)
        except User_Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )
      

        # PUT
        if request.method == 'PUT':
            serializer = AccountSerializer(
                account,
                data=request.data
            )

        # PATCH
        elif request.method == 'PATCH':
            serializer = AccountSerializer(
                account,
                data=request.data,
                partial=True
            )
            # DELETE
    elif request.method == 'DELETE':

        try:
            account = User_Account.objects.get(id=id)
        except User_Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        account.delete()
        return Response(
            {"message": "Account deleted successfully"},
            status=status.HTTP_200_OK
        )
      

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
def Forgotpassword(request):

    if request.method == 'POST':

        email = request.POST.get("email")
        

        print("EMAIL ENTERED:", email)

        print(
            "REGISTERED USERNAMES:",
            list(User.objects.values_list("username", flat=True))
        )

        if User.objects.filter(username__iexact=email).exists():

            otp = random.randint(100000, 999999)

            request.session['reset_username'] = email
            request.session['reset_otp'] = otp

            print("OTP:", otp)

            return redirect("verify_otp")

        else:

            print("EMAIL NOT FOUND")

            return render(
                request,
                'ForgotPassword.html',
                {
                    "error": "Email is not registered"
                }
            )

    return render(request, 'ForgotPassword.html')

@csrf_exempt
def Verify_OTP(request):
    if request.method == 'POST':
        entered_otp=request.POST.get("otp")
        stored_otp=request.session.get('reset_otp')
        username=request.session.get("reset_username")

        print("ENTERED OTP:", entered_otp)
        print("STORED OTP:", stored_otp)
        print("RESET USERNAME:", username  )
        if str(entered_otp) == str(stored_otp):

            # OTP is correct
            request.session['otp_verified'] = True

            return redirect("reset_password")

        else:

            return render(
                request,
                'Verify_Otp.html',
                {
                    "error": "Invalid OTP. Please try again."
                }
            )
    return render(request, 'Verify_Otp.html')

@csrf_exempt
def ResetPassword(request):
    if request.method == 'POST':
        new_password= request.POST.get("new_password")
        confirm_password=request.POST.get("confirm_password")
        if new_password != confirm_password:
            return render(request,'ResetPassword.html', context={"error":"Password do not match"})
        messages.success(request,"Your password has been changed successfully")
        errors=[]
        if len(new_password) < 8 :
                errors.append("Password  must be  at least 8 characters")
        if not re.search(r"[A-Z]", new_password):
                errors.append("Password must contain at least  one Uppercase Letter.")
        if not re.search(r"[a-z]", new_password):
                errors.append("Password must contain at least one Lowercase Letter .")
        if not re.search(r"[0-9]",new_password):
                errors.append("Password must  contain  at least one number .")
        if not re.search(r"[@#$!*%&]",new_password):
                errors.append("password must contain at least one special  character such as @,#,$,!,*,&")
        if errors:
                return  render(request, 'ResetPassword.html',context={"errors":errors})
        username = request.session.get('reset_username')

        if not username:
            return redirect('forgot')
        user=User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        del request.session["reset_username"]
        print(new_password)
        return redirect("login-page")
    return render(request,'ResetPassword.html')    



