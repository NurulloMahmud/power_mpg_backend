from .models import Store, StorePrice
from rest_framework import serializers


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"

class StorePriceReadSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    class Meta:
        model = StorePrice
        fields = "__all__"

class StorePriceWriteSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    class Meta:
        model = StorePrice
        fields = "__all__"
