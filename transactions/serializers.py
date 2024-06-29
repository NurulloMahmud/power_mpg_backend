from rest_framework import serializers
from .models import Transaction


class TransactionListAdminSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()
    card = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id", "card", "company", "driver", "store", "state","date","item", "unit_number", "retail_price", "client_price",
            "company_price", "quantity", "retail_amount", "client_amount", "company_amount", "client_profit", "company_profit", "transaction_fee", "debt"
        ]

    def get_store(self, obj):
        return obj.store.name

    def get_card(self, obj):
        return obj.card.card_number

    def get_state(self, obj):
        return obj.store.state

class TransactionListSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()
    card = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id", "card", "company", "driver", "store", "state", "date", "item", "unit_number", "retail_price", "client_price", 
            "quantity", "retail_amount", "client_amount",  "client_profit", "transaction_fee", "debt"
        ]

    def get_store(self, obj):
        return obj.store.name

    def get_card(self, obj):
        return obj.card.card_number

    def get_state(self, obj):
        return obj.store.state
