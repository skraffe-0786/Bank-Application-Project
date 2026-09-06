from rest_framework import serializers
from .models import User_Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_Account
        fields= '__all__'