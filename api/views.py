from rest_framework.response import Response

from rest_framework.decorators import api_view

from base.models import Item
from .serializers import ItemSerializer, UserSerializer

from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

@api_view(['GET'])
def getAllItems(request):
    items = Item.objects.all()
    serialized_items = ItemSerializer(items, many=True)
    return Response(serialized_items.data)

@api_view(['POST'])
def addItem(request):
    
    serialized_item = ItemSerializer(data = request.data)
    if serialized_item.is_valid():
        serialized_item.save()
    return Response(serialized_item.data)


# AUTHENTICATION
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        #hash password
        user.set_password(request.data['password'])
        user.save()
        
        token = Token.objects.create(user=user)
        return Response({"token":token.key, "user":serializer.data} )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username= request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail: ":"Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    
    token,created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token ":token.key, "user": serializer.data})

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Passed for {}".format(request.user.email))

@api_view(['GET'])
def getAllUsers(request):
    users = User.objects.all()
    serialized_users = UserSerializer(users, many=True)
    
    return Response(serialized_users.data)