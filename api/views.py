from rest_framework.response import Response

from rest_framework.decorators import api_view

from base.models import Item
from .serializers import ItemSerializer

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