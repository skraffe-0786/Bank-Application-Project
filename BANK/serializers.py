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

class TransferSerializer(serializers.Serializer):

    sender = serializers.CharField()
    receiver = serializers.CharField()
    amount = serializers.DecimalField(
        max_digits=100,
        decimal_places=1
    )

    def validate(self, attrs):

        sender = attrs["sender"]
        receiver = attrs["receiver"]
        amount = attrs["amount"]

        if sender == receiver:
            raise serializers.ValidationError(
                "You cannot transfer to your own account."
            )

        if amount <= 0:
            raise serializers.ValidationError(
                "Transfer amount must be greater than zero."
            )

        return attrs