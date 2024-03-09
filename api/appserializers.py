from rest_framework import serializers
from django.contrib.auth.models import User
from  .models import CustomUser
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
                  'email', 'first_name', 'last_name', "username","profile", "phone")
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

