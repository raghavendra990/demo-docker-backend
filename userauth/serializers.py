

from rest_framework.serializers import (
    Serializer, ModelSerializer, SerializerMethodField, UUIDField,
    CharField, ChoiceField, EmailField, BooleanField, ListField, JSONField, DateField)

from phonenumber_field.serializerfields import PhoneNumberField
from .models import UserModel

class RegisterSerializer(Serializer):  # pylint: disable=abstract-method
    """
    Register serializer
    """
    firstname = CharField(max_length=50,  required=True, trim_whitespace=True)
    lastname = CharField(max_length=50,  required=True, trim_whitespace=True)
    password = CharField(max_length=16,  required=True)
    dob = DateField(required=True)
    phone_number = PhoneNumberField(required=True, trim_whitespace=True)

class LoginSerializer(Serializer):  # pylint: disable=abstract-method
    """
    Login serializer
    """
    phone_number = PhoneNumberField(required=True, trim_whitespace=True)
    password = CharField(max_length=16,  required=True)

    
class UserDetailsSerializer(ModelSerializer):  # pylint: disable=abstract-method
    """
    UserDetails serializer
    """
    class Meta:
        model = UserModel
        fields = ('firstname', 'lastname', 'phone_number', 'dob')
   