from rest_framework import serializers
from django.contrib.auth.models import User
from  .models import CustomUser, Product, Cart, Vtu_transaction
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
#from models import Subscription, UserProfile from .appserializers import  UserSerializer



class RegisterSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True,)# validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ( 'password',
                  'email', 'first_name', 'last_name', "username","profile", "phone", "wallet")
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }



class Productserializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ["product_id", "product_price", "product_category", "image", "product_desc" ] 





class Cartserializer(serializers.ModelSerializer):
    class Meta:
        model= Cart
        fields = ["id", "item", "user_id", "quantity"]


class Vtuserializer(serializers.ModelSerializer):
    class Meta:
        model= Vtu_transaction
        fields = ["id", "transaction_type","phone", "ref_id", "amount", "user_id", "transaction_time"]