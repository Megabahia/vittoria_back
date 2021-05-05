from apps.ADM.vittoria_catalogo.models import Catalogo
from apps.ADM.vittoria_catalogo.serializers import CatalogoSerializer,CatalogoTipoSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
#CRUD catalogo
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def catalogo_list(request):

    if request.method == 'GET':
        catalogo= Catalogo.objects.filter(state=1)
        serializer = CatalogoSerializer(catalogo, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def catalogo_create(request):
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['created_at'] = str(now)
        if 'updated_at' in request.data:
            request.data.pop('updated_at')
        serializer = CatalogoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def catalogo_findOne(request, pk):
    try:
        catalogo = Catalogo.objects.get(pk=pk, state=1)
    except Catalogo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'GET':
        serializer = CatalogoSerializer(catalogo)
        return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#ACTUALIZAR 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def catalogo_update(request, pk):
    try:
        catalogo = Catalogo.objects.get(pk=pk, state=1)
    except Catalogo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['updated_at'] = str(now)
        if 'created_at' in request.data:
            request.data.pop('created_at')
        serializer = CatalogoSerializer(catalogo, data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def catalogo_delete(request, pk):
    try:
        catalogo = Catalogo.objects.get(pk=pk, state=1)
    except Catalogo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'DELETE':
        now = timezone.localtime(timezone.now())
        serializer = CatalogoSerializer(catalogo, data={'state': '0','updated_at':str(now)},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#GET ESTADOS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estado_list(request):

    if request.method == 'GET':
        catalogo= Catalogo.objects.filter(state=1,tipo="ESTADO")
        serializer = CatalogoTipoSerializer(catalogo, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#GET PAISES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pais_list(request):

    if request.method == 'GET':
        catalogo= Catalogo.objects.filter(state=1,tipo="PAIS")
        serializer = CatalogoTipoSerializer(catalogo, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)