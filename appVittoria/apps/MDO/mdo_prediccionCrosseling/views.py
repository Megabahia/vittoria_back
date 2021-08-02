from apps.MDO.mdo_prediccionCrosseling.models import (
    PrediccionCrosseling, Detalles
)
from apps.MDO.mdo_prediccionCrosseling.serializers import (
    PrediccionCrosselingListSerializer, PrediccionCrosselingSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
#excel
import openpyxl
#logs
from apps.ADM.vittoria_logs.methods import createLog,datosTipoLog, datosPrediccionCrosselingMDO
#declaracion variables log
datosAux=datosPrediccionCrosselingMDO()
datosTipoLogAux=datosTipoLog()
#asignacion datos modulo
logModulo=datosAux['modulo']
logApi=datosAux['api']
#asignacion tipo de datos
logTransaccion=datosTipoLogAux['transaccion']
logExcepcion=datosTipoLogAux['excepcion']
#CRUD PRODUCTOS
#LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prediccionCrosseling_list(request):
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
            if request.data['inicio']!='':
                filters['fechaPredicciones__gte'] = str(request.data['inicio'])   
            if request.data['fin']!='':
                filters['fechaPredicciones__lte'] = str(request.data['fin'])              
            if 'cliente' in request.data:
                if request.data['cliente']!='':
                    filters['cliente'] = str(request.data['cliente'])     
            if 'negocio' in request.data:
                if request.data['negocio']!='':
                    filters['negocio'] = str(request.data['negocio'])     
            if 'identificacion' in request.data:
                if request.data['identificacion']!='':
                    filters['identificacion__icontains'] = str(request.data['identificacion'])     

            #Serializar los datos
            query = PrediccionCrosseling.objects.filter(**filters).order_by('-created_at')
            serializer = PrediccionCrosselingListSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

#ENCONTRAR UNO
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def productos_findOne(request, pk):
#     timezone_now = timezone.localtime(timezone.now())
#     logModel = {
#         'endPoint': logApi+'listOne/',
#         'modulo':logModulo,
#         'tipo' : logExcepcion,
#         'accion' : 'LEER',
#         'fechaInicio' : str(timezone_now),
#         'dataEnviada' : '{}',
#         'fechaFin': str(timezone_now),
#         'dataRecibida' : '{}'
#     }
#     try:
#         try:
#             query = Productos.objects.get(pk=pk, state=1)
#         except Productos.DoesNotExist:
#             err={"error":"No existe"}  
#             createLog(logModel,err,logExcepcion)
#             return Response(err,status=status.HTTP_404_NOT_FOUND)
#         #tomar el dato
#         if request.method == 'GET':
#             serializer = PrediccionCrosselingSerializer(query)
#             createLog(logModel,serializer.data,logTransaccion)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#     except Exception as e: 
#             err={"error":'Un error ha ocurrido: {}'.format(e)}  
#             createLog(logModel,err,logExcepcion)
#             return Response(err, status=status.HTTP_400_BAD_REQUEST)

#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prediccionCrosseling_create(request):
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
        
            serializer = PrediccionCrosselingSerializer(data=request.data)
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
