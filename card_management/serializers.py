from rest_framework import serializers
from .models import Card, CardDriverHistory
from datetime import datetime


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
    from users.models import Company
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        card = Card.objects.create(**validated_data)
        if card.driver is not None:
            CardDriverHistory.objects.create(
                card=card.card_number,
                driver=card.driver,
                company=card.company,
            )
        return card

    def update(self, instance, validated_data):
        # check if the driver is changing
        driver = validated_data.get("driver")
        if driver is not None and driver != instance.driver:
            old_card_history = CardDriverHistory.objects.filter(
                card=instance.card_number,
                end_date__isnull=True,
            ).first()
            if old_card_history is not None:
                old_card_history.end_date = datetime.now()
                old_card_history.save()
                
            # create new history
            CardDriverHistory.objects.create(
                card=instance.card_number,
                driver=driver,
                company=instance.company,
            )
        return super().update(instance, validated_data)

class CardDriverHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDriverHistory
        fields = "__all__"
        