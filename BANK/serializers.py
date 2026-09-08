from rest_framework import serializers
from .models import User_Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_Account
        fields= '__all__'
    def validate_Current_Balance(self,value):
        if value < 0 :
            raise serializers.ValidationError(
                "Balance  cannot be  negative "
            )
        return value