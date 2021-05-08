from apps.ADM.vittoria_catalogo.models import Catalogo
from apps.ADM.vittoria_catalogo.serializers import CatalogoSerializer,CatalogoHijoSerializer,CatalogoFiltroSerializer,CatalogoTipoSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
#logs
from apps.ADM.vittoria_logs.methods import createLog,datosCatalogo,datosTipoLog
#declaracion variables log
datosAux=datosCatalogo()
datosTipoLogAux=datosTipoLog()
#asignacion datos modulo
logModulo=datosAux['modulo']
logApi=datosAux['api']
#asignacion tipo de datos
logTransaccion=datosTipoLogAux['transaccion']
logExcepcion=datosTipoLogAux['excepcion']
#CRUD catalogo
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def catalogo_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'list/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'LEER',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            #paginacion
            page_size=int(request.data['page_size'])
            page=int(request.data['page'])
            offset = page_size* page
            limit = offset + page_size
            #Filtros
            filters={"state":"1"}
            if 'nombre' in request.data:
                if request.data['nombre']!='':
                    filters['nombre__startswith'] = str(request.data['nombre'])
            if 'idTipo' in request.data:
                if request.data['idTipo']!=0:
                    filters['idPadre__id'] = int(request.data['idTipo'])
          
            #Serializar los datos
            query = Catalogo.objects.filter(**filters).order_by('-created_at')
            serializer = CatalogoHijoSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def catalogo_create(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'create/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'CREAR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            #asigno el idTipo al idPadre
            request.data['idPadre']=request.data.pop('idTipo')
            serializer = CatalogoSerializer(data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def catalogo_findOne(request, pk):
    try:
        try:
            catalogo = Catalogo.objects.get(pk=pk, state=1)
        except Catalogo.DoesNotExist:
            err={"error":"No existe"}  
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':
            serializer = CatalogoHijoSerializer(catalogo)
            return Response(serializer.data)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
    




#ACTUALIZAR 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def catalogo_update(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'update/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'ESCRIBIR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:
            catalogo = Catalogo.objects.get(pk=pk, state=1)
        except Catalogo.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            request.data['updated_at'] = str(timezone_now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            #asigno el idTipo al idPadre
            if 'idTipo' in request.data:
                request.data['idPadre']=request.data.pop('idTipo')
            serializer = CatalogoSerializer(catalogo, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
                return Response(serializer.data)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 
   
#ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def catalogo_delete(request, pk):
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'delete/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'BORRAR',
        'fechaInicio' : str(nowDate),
        'dataEnviada' : '{}',
        'fechaFin': str(nowDate),
        'dataRecibida' : '{}'
    }
    try:
        try:
            catalogo = Catalogo.objects.get(pk=pk, state=1)
        except Catalogo.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'DELETE':
            serializer = CatalogoSerializer(catalogo, data={'state': '0','updated_at':str(nowDate)},partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
                return Response(serializer.data,status=status.HTTP_200_OK)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#GET ESTADOS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estado_list(request):

    if request.method == 'GET':
        try:
            catalogo= Catalogo.objects.filter(state=1,idPadre__tipo="ESTADO",idPadre__state=1)
            serializer = CatalogoFiltroSerializer(catalogo, many=True)
            return Response(serializer.data)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
      


#GET PAISES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pais_list(request):

    if request.method == 'GET':
        try:
            catalogo= Catalogo.objects.filter(state=1,idPadre__tipo="PAIS",idPadre__state=1)
            serializer = CatalogoFiltroSerializer(catalogo, many=True)
            return Response(serializer.data)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

#GET TIPO DE PARAMETRIZACIONES/CATÁLOGO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tipo_list(request):

    if request.method == 'GET':
        try:
            catalogo= Catalogo.objects.filter(state=1,idPadre__isnull=True).exclude(tipo='Log')
            serializer = CatalogoTipoSerializer(catalogo, many=True)
            return Response(serializer.data)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
        