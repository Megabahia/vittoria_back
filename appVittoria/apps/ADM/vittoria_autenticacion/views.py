from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from apps.ADM.vittoria_usuarios.models import Usuarios
from apps.ADM.vittoria_usuarios.serializers import UsuarioSerializer, UsuarioCrearSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login,logout,authenticate
#token login
from rest_framework.authtoken.views import ObtainAuthToken
from apps.ADM.vittoria_autenticacion.models import Token
from apps.ADM.vittoria_autenticacion.auth import token_expire_handler,expires_in, deleteExpiredTokens
from django.utils import timezone
#logs
from apps.ADM.vittoria_logs.methods import createLog,datosAuth,datosTipoLog
#permisos
from apps.ADM.vittoria_roles.models import Roles
from apps.ADM.vittoria_acciones.models import Acciones, AccionesPermitidas, AccionesPorRol
#declaracion variables log
datosAux=datosAuth()
datosTipoLogAux=datosTipoLog()
#asignacion datos modulo
logModulo=datosAux['modulo']
logApi=datosAux['api']
#asignacion tipo de datos
logTransaccion=datosTipoLogAux['transaccion']
logExcepcion=datosTipoLogAux['excepcion']



 
class login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        #log
        timezone_now = timezone.localtime(timezone.now())
        logModel = {
            'endPoint': logApi+'login/',
            'modulo':logModulo,
            'tipo' : logExcepcion,
            'accion' : 'LEER',
            'fechaInicio' : str(timezone_now),
            'dataEnviada' : '{}',
            'fechaFin': str(timezone_now),
            'dataRecibida' : '{}'
        }
        try:
            logModel['dataEnviada'] = str(request.data)
            serializer = self.serializer_class(data=request.data,
                                        context={'request': request})
            if serializer.is_valid():
                user = serializer.validated_data['user']
                if user.state==1:
                    token= Token.objects.create(user=user)
                    #ELIMINAR USUARIOS EXPIRADOS
                    deleteExpiredTokens()
                    #inner join para sacar los permisos urls
                    acciones=AccionesPermitidas.objects.extra(tables=['vittoria_acciones_acciones','vittoria_acciones_accionesporrol'], 
                    where=['vittoria_acciones_acciones.id=vittoria_acciones_accionespermitidas.idAccion_id',
                            'vittoria_acciones_acciones.state=1',
                            'vittoria_acciones_accionesporrol.idAccion_id=vittoria_acciones_acciones.id',
                            'vittoria_acciones_accionesporrol.idRol_id='+str(user.idRol.id)
                    ],
                    select={'url': 'vittoria_acciones_accionespermitidas.url'})
                    userSerializer = UsuarioCrearSerializer(user)
                    data={
                        'token': token.key,
                        'id': user.pk,
                        'full_name': user.nombres+" "+user.apellidos,
                        'usuario': userSerializer.data,
                        'email': user.email,
                        'tokenExpiracion': expires_in(token),
                        'permisos':[]
                    }
                    for accion in acciones:
                        data['permisos'].append({'url':str(accion)})
                    createLog(logModel,data,logTransaccion)
                    return Response(data,status=status.HTTP_200_OK)        
                else:
                    err={'error':'el usuario no existe!'}
                    createLog(logModel,err,logExcepcion)
                    return Response(err,status=status.HTTP_404_NOT_FOUND)  
            else:
                createLog(logModel,serializer.errors,logExcepcion)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
            