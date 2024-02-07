from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import jwt
from datetime import datetime
from .log import LOGGER, raise_400
from .authentication import IsTokenValid
from .models import UserModel, BlackListedToken
from .serializers import LoginSerializer, RegisterSerializer, UserDetailsSerializer

# Create your views here.

USER_ALREADY_PRESENT = "User Already Exist."
USER_NOT_EXIST = "User Does not Exist."

INVALID_LOGIN = "Invalid phonenumber or Password."
class RegisterAPIView(APIView):

    """
    Register API
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def get_serializer(self, *args, **kwargs):
        """Return view serializer class"""
        return self.serializer_class(*args, **kwargs)

    def _check_user_exist(self, phone_number):
        user = UserModel.objects.filter(phone_number=phone_number)
        if user:
            raise_400(USER_ALREADY_PRESENT)


    def post(self, request):
        serializer  = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = str(serializer.validated_data['phone_number'])

        self._check_user_exist(phone_number)
        user_obj = UserModel.register(data=serializer.data)

        payload = {"id": user_obj.id, "phone_number": user_obj.phone_number, "firstname": user_obj.firstname, "lastname": user_obj.lastname, 'dob': user_obj.dob}
        return Response(status=200, data=payload)

class LoginAPIView(APIView):

    """
    Login API
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get_serializer(self, *args, **kwargs):
        """Return view serializer class"""
        return self.serializer_class(*args, **kwargs)

    def _check_user(self, phone_number):
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            if not user:
                raise_400(USER_NOT_EXIST)
        except Exception as e:
            raise_400(USER_NOT_EXIST)
        return user
    
    def generate_jwt_token(self, data):
        data['created_at'] = str(datetime.utcnow())

        return 'JWT {}'.format(jwt.encode(data,settings.JWT_SECRET_KEY, algorithm='HS256'))


    def post(self, request):
        serializer  = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = str(serializer.validated_data['phone_number'])
        password = serializer.validated_data['password']

        user = self._check_user(phone_number)

        verified_check = UserModel.verify_password(user.password, password, phone_number)

        if verified_check:
            token = self.generate_jwt_token({"phone_number": phone_number, "id": str(user.id) })
        else:
            return Response(status=403, data={"message": INVALID_LOGIN})
        return Response(status=200, data={"token":token})

class LogoutAPIView(APIView):

    """
    Logiout API
    """

    permission_classes = [IsAuthenticated, IsTokenValid]
    # serializer_class = LoginSerializer

    # def get_serializer(self, *args, **kwargs):
    #     """Return view serializer class"""
    #     return self.serializer_class(*args, **kwargs)


    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user_id = request.user.user_id
        user_obj = UserModel(id=user_id)
        blt_obj = BlackListedToken(token=token, user=user_obj)
        blt_obj.save()
        return Response(status=200, data={"messge": "logout successfully"})

class UserDetailsAPIView(APIView):

    """
    UserDetails API
    """

    permission_classes = [IsAuthenticated, IsTokenValid]
    serializer_class = UserDetailsSerializer

    def get_serializer(self, *args, **kwargs):
        """Return view serializer class"""
        return self.serializer_class
    
    def get(self, request):
        serializers = self.get_serializer()
        user_id = request.user.user_id
        user_obj = UserModel.objects.get(id=user_id)
        data = serializers(user_obj)
        return Response(status=200, data=data.data)
