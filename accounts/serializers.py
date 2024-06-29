from rest_framework import serializers
from .models import AccountType



class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = "__all__"

