from rest_framework import serializers
from .models import CustomUser, Company


class CompanySerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = "__all__"

    def get_users(self, obj):
        users = CustomUser.objects.filter(company=obj).count()
        return users

    def create(self, validated_data):
        category = validated_data.get('price_category', 0)
        try:
            category = int(category)
        except:
            raise serializers.ValidationError('Price category must be an integer')
        if category < 1 or category > 5:
            raise serializers.ValidationError('Price category must be between 1 and 5')
        return super().create(validated_data)

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = CustomUser
        fields = ["id", "username", "company", "role", "is_active"]

class UserUpdateSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), allow_null=True)
    class Meta:
        model = CustomUser
        fields = ["company", "role", "is_active"]

class CurrentUserSerializer(serializers.ModelSerializer):
    company_price_category = serializers.IntegerField(source='company.price_category', read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "company_price_category", "role", "is_active"]
