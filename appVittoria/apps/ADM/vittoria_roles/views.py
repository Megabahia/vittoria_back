
from apps.ADM.vittoria_roles.models import Roles
from apps.ADM.vittoria_acciones.models import Acciones, AccionesPermitidas, AccionesPorRol
from apps.ADM.vittoria_acciones.serializers import AccionesSerializer,AccionesPadreSerializer, AccionesPermitidasSerializer, AccionesPorRolSerializer
from apps.ADM.vittoria_roles.serializers import RolSerializer,RolFiltroSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
#logs
from apps.ADM.vittoria_logs.methods import createLog,datosRoles,datosTipoLog
#declaracion variables log
datosAux=datosRoles()
datosTipoLogAux=datosTipoLog()
#asignacion datos modulo
logModulo=datosAux['modulo']
logApi=datosAux['api']
#asignacion tipo de datos
logTransaccion=datosTipoLogAux['transaccion']
logExcepcion=datosTipoLogAux['excepcion']

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def rol_list(request):
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'list/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'LEER',
        'fechaInicio' : str(nowDate),
        'dataEnviada' : '{}',
        'fechaFin': str(nowDate),
        'dataRecibida' : '{}'
    }
    try:
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            #paginacion
            page_size=int(request.data['page_size'])
            page=int(request.data['page'])
            offset = page_size* page
            limit = offset + page_size
            #Serializar los datos
            rol = Roles.objects.filter(state=1).order_by('-created_at')
            serializer = RolSerializer(rol[offset:limit], many=True)
            new_serializer_data={'cont': rol.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#EXPORTAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rol_listExport(request):
    try:
        if request.method == 'POST':
            #Serializar los datos
            rol = Roles.objects.filter(state=1).order_by('-created_at')
            serializer = RolSerializer(rol, many=True)
            new_serializer_data={'cont': rol.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rol_create(request):
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'create/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'CREAR',
        'fechaInicio' : str(nowDate),
        'dataEnviada' : '{}',
        'fechaFin': str(nowDate),
        'dataRecibida' : '{}'
    }
    try:
        nowDate = timezone.localtime(timezone.now())
        rolId=0
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            #asigno datos del rol
            rolCrear=request.data['rol']
                #agrego la fecha en la que va ser guardada
            rolCrear['created_at'] = str(nowDate)
            if 'updated_at' in request.data:
                rolCrear.pop('updated_at')
            #Guardo los roles
            serializer = RolSerializer(data=rolCrear)
            if serializer.is_valid():
                serializer.save()
                #Asigno id del rol creado para usarlo en las acciones
                rolId=int(serializer.data['id'])
            else:
                createLog(logModel,serializer.errors,logExcepcion)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #Valido que existan las acciones
            if 'acciones' in request.data:
                accionesCrear=request.data['acciones']
                #recorro los padres(modulos)
                #recorro el json de acciones, busco el id de la accion del modulo, Leer, Escribir,etc, por último lo almaceno con los datos 
                for keyPadre, valuePadre in accionesCrear.items():
                    nombrePadre=str(keyPadre) 
                    for keyHijo, valueHijo in valuePadre.items():
                        nombreHijo,estado=str(keyHijo),int(valueHijo)
                        accion=Acciones.objects.filter(idAccionPadre__nombre=nombrePadre,nombre=nombreHijo).only('id').first()
                        #creo la accion
                        AccionesPorRol.objects.create(idAccion_id=int(accion.id),idRol_id=rolId,state=estado,created_at=nowDate)
                dataExitosa={"mensaje":"rol y acciones creadas exitosamente","rol":serializer.data,"acciones":accionesCrear}
                createLog(logModel,dataExitosa,logTransaccion)
                return Response(dataExitosa, status=status.HTTP_201_CREATED)
            else:
                err={"error":"El rol ha sido creado pero sin ninguna acción!","rol":serializer.data}  
                createLog(logModel,err,logExcepcion)
                return Response(err, status=status.HTTP_400_BAD_REQUEST)  
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 


      


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rol_update(request,pk):
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'update/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'ESCRIBIR',
        'fechaInicio' : str(nowDate),
        'dataEnviada' : '{}',
        'fechaFin': str(nowDate),
        'dataRecibida' : '{}'
    }
    try:
        rolId=0
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            #asigno los datos del rol
            rolUpdate=request.data['rol']
            try:
                rol = Roles.objects.get(pk=pk, state=1)
            except Roles.DoesNotExist:
                err={"err":"El rol no existe"}
                createLog(logModel,err,logExcepcion)
                return Response(err,status=status.HTTP_404_NOT_FOUND)
            rolId=int(rol.id)
            #agrego la fecha actualizar
            rolUpdate['updated_at'] = str(nowDate)
            if 'created_at' in request.data:
                rolUpdate.pop('created_at')
            serializer = RolSerializer(rol, data=rolUpdate,partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                createLog(logModel,serializer.errors,logExcepcion)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            #Valido que existan las acciones
            if 'acciones' in request.data:
                accionesUpdate=request.data['acciones']
                #recorro los padres(modulos)
                #recorro el json de acciones, busco el id de la accion del modulo, Leer, Escribir,etc, por último actualizo los datos
                for keyPadre, valuePadre in accionesUpdate.items():
                    nombrePadre=str(keyPadre) 
                    for keyHijo, valueHijo in valuePadre.items():
                        nombreHijo,estado=str(keyHijo),int(valueHijo)
                        accion=Acciones.objects.filter(idAccionPadre__nombre=nombrePadre,nombre=nombreHijo).only('id').first()
                        #creo la accion
                        AccionesPorRol.objects.filter(idAccion_id=int(accion.id),idRol_id=rolId).update(state=estado,updated_at=nowDate)
                #retorno el rol creado con sus acciones
                dataExitosa={"mensaje":"rol y acciones actualizadas exitosamente","rol":serializer.data,"acciones":accionesUpdate}
                createLog(logModel,dataExitosa,logTransaccion) 
                return Response(dataExitosa, status=status.HTTP_201_CREATED)
            else:
                err={"error":"El rol ha sido actualizado pero las acciones no!","rol":serializer.data}  
                createLog(logModel,err,logExcepcion) 
                return Response(err, status=status.HTTP_400_BAD_REQUEST)  
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion) 
        return Response(err, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rol_findOne(request, pk):
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'listOne/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'LEER',
        'fechaInicio' : str(nowDate),
        'dataEnviada' : '{}',
        'fechaFin': str(nowDate),
        'dataRecibida' : '{}'
    }
    try:
        rolId=0
        accionesList={}
        if request.method == 'GET':
            logModel['dataEnviada'] = str(request.data)
            #Verifico si existe el rol
            try:
                rol = Roles.objects.get(pk=pk, state=1)
            except Roles.DoesNotExist:
                err={"err":"El rol no existe"}
                createLog(logModel,err,logExcepcion) 
                return Response(err,status=status.HTTP_404_NOT_FOUND)
            #tomo los datos del rol
            serializer = RolFiltroSerializer(rol)
            rolId=int(serializer.data['id'])
            #recorro los padres(modulos)
            for accionPadre in Acciones.objects.filter(idAccionPadre__isnull=True):
                accionesCrud={} #guardo las acciones leer,escribir,editar,borrar
                #recorro las acciones de cada padre y las almaceno 
                for accionHijo in AccionesPorRol.objects.filter(idRol_id=rolId, idAccion__idAccionPadre__nombre=str(accionPadre.nombre)).order_by('id'):
                    accionesCrud[str(accionHijo.idAccion.nombre)]=str(accionHijo.state)
                #asigno el crud a la lista
                accionesList[str(accionPadre.nombre)]=accionesCrud
            #envio la data
            dataExitosa={"rol":serializer.data,"acciones":accionesList}
            return Response(dataExitosa, status=status.HTTP_201_CREATED)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion) 
        return Response(err, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def rol_delete(request, pk):
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
            rol = Roles.objects.get(pk=pk, state=1)
        except Roles.DoesNotExist:
            err={"err":"El rol no existe"}
            createLog(logModel,err,logExcepcion) 
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        if request.method == 'DELETE':
            serializer = RolSerializer(rol, data={'state': '0','updated_at':str(nowDate)},partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion) 
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion) 
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 

#LISTA MODULOS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rol_listAccionPadre(request):
    try:
        if request.method == 'GET':
            #Serializar los datos
            query = Acciones.objects.filter(idAccionPadre__isnull=True,state=1)
            serializer = AccionesPadreSerializer(query,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#ROLES ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rol_listFiltro(request):
    try:
        if request.method == 'GET':
            rol= Roles.objects.filter(state=1)
            serializer = RolFiltroSerializer(rol, many=True)
            return Response(serializer.data)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 