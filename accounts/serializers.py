from rest_framework import serializers
from .models import AccountType, Account, Payment



class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = "__all__"

class PaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class PaymentReadSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    class Meta:
        model = Payment
        fields = "__all__"

    def get_account(self, obj):
        return obj.account.company.name
