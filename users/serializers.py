from rest_framework import serializers
from .models import CustomUser, Company, CompanyStatus
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

class CompanyWriteSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=CompanyStatus.objects.all(), allow_null=True)

    class Meta:
        model = Company
        fields = "__all__"

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

#   customizing simple jwt to return user's role
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['role'] = self.user.role

        return data

