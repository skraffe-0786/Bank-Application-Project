from django.contrib import admin
from.models import Bank
from.models import USER_Role
from.models import User_Account
from.models import Transcations

# Register your models here.
admin.site.register(Bank)
admin.site.register(USER_Role)
admin.site.register(User_Account)
admin.site.register(Transcations)