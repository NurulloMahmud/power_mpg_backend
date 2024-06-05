from rest_framework import serializers
from .models import Card, CardDriverHistory


class CardReadSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = "__all__"

    def get_company(self, obj):
        from users.models import Company
        company_obj = Company.objects.get(id=obj.company.id)
        return company_obj.name

class CardWriteSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset="users.Company.objects.all()")
    class Meta:
        model = Card
        fields = "__all__"

class CardDriverHistorySerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    class Meta:
        model = CardDriverHistory
        fields = "__all__"
    
    def get_company(self, obj):
        from users.models import Company
        company_obj = Company.objects.get(id=obj.company.id)
        return company_obj.name
