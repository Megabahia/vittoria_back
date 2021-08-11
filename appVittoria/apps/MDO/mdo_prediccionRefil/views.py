from django.db.models import Avg
from apps.MDO.mdo_prediccionRefil.models import (
    PrediccionRefil, Detalles
)
from apps.MDO.mdo_prediccionRefil.serializers import (
    PrediccionRefilListSerializer, PrediccionRefilSerializer, DetallesImagenesSerializer,
    PrediccionRefilProductosSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
import datetime
# Request
import requests
from apps.config import config
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
def prediccionRefil_list(request):
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
                    filters['cliente__isnull'] = False        
            if 'negocio' in request.data:
                if request.data['negocio']!='':
                    filters['negocio__isnull'] = False   
            if 'identificacion' in request.data:
                if request.data['identificacion']!='':
                    filters['identificacion__icontains'] = str(request.data['identificacion'])    

            #Serializar los datos
            query = PrediccionRefil.objects.filter(**filters).order_by('-created_at')
            serializer = PrediccionRefilListSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

#ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalles_list(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'productosImagenes/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'LEER',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:
            print('holaaa')
            query = Detalles.objects.filter(prediccionRefil=pk, state=1)
            print(query)
        except Detalles.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':            
            serializer = DetallesImagenesSerializer(query, many=True)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prediccionRefil_create(request):
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
            # Preparar prediccion
            auth_token=request.META['HTTP_AUTHORIZATION']
            hed = {'Authorization': auth_token}
                                    
            detalles = request.data.pop('detalles')
            for producto in detalles:
                # Consultar refil
                data = {"producto": producto['codigo']}
                r = requests.post(config.API_BACK_END+'mdp/productos/producto/refil/',data=data,headers=hed)            
                date = datetime.strptime(request.data['fecha'], "%Y-%m-%d").date()
                prediction_date = date + timedelta(days=r.json()[0]['refil'])                
                request.data['fechaPredicciones'] = prediction_date
                request.data['detalles'] = [producto]
                serializer = PrediccionRefilSerializer(data=request.data)                
                if serializer.is_valid():                    
                    serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
            # fin prediccion

            # Termina for    
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

#ENCONTRAR UNA PREDICCION REFIL
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prediccion_refil_listOne(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'prediccionRefil/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'LEER',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:
            query = Detalles.objects.filter(prediccionRefil=pk, state=1)
        except Detalles.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':
            today = datetime.date.today()
            prediccionUltimoTotal = PrediccionRefil.objects.filter(pk=pk).aggregate(ultimoTotal=Avg('total'))
            prediccionTotalAnio = PrediccionRefil.objects.filter(created_at__year=today.year).aggregate(ultimoTotal=Avg('total'))
            prediccionTotalMes = PrediccionRefil.objects.filter(created_at__month=today.month).aggregate(ultimoTotal=Avg('total'))         
            serializer = PrediccionRefilProductosSerializer(query, many=True)
            auth_token=request.META['HTTP_AUTHORIZATION']
            hed = {'Authorization': auth_token}
            if query[0].prediccionRefil.cliente is not None:
                r = requests.get(config.API_BACK_END+'mdm/clientes/prediccionRefil/listOne/'+str(query[0].prediccionRefil.cliente),headers=hed) 
                data = {'cliente': r.json(), 'productos': serializer.data
                , 'comprasMensuales': prediccionTotalMes['ultimoTotal']
                , 'comprasAnuales': prediccionTotalAnio['ultimoTotal']
                , 'ultimoTotal': prediccionUltimoTotal['ultimoTotal']}
            else:
                r = requests.get(config.API_BACK_END+'mdm/negocios/prediccionRefil/listOne/'+str(query[0].prediccionRefil.negocio),headers=hed) 
                data = {'negocio': r.json(), 'productos': serializer.data
                , 'comprasMensuales': prediccionTotalMes['ultimoTotal']
                , 'comprasAnuales': prediccionTotalAnio['ultimoTotal']
                , 'ultimoTotal': prediccionUltimoTotal['ultimoTotal']}
            createLog(logModel,serializer.data,logTransaccion)
            return Response(data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


