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

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class UserListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = CustomUser
        fields = ["username", "company", "role"]

class UserUpdateSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), allow_null=True)
    class Meta:
        model = CustomUser
        fields = ["company", "role", "is_active"]
