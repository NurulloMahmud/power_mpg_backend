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

class AccountWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

class AccountViewSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    account_type = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ["company", "account_type", "balance"]

    def get_company(self, obj):
        return obj.company.name

    def get_account_type(self, obj):
        return obj.account_type.name
