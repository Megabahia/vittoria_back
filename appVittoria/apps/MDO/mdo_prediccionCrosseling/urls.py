from django.urls import path,include
from apps.MDO.mdo_prediccionCrosseling.views import(
	prediccionCrosseling_list, prediccionCrosseling_create
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'prediccionCrosseling'

urlpatterns = [
	#parametrizaciones	
	path('list/', prediccionCrosseling_list, name="prediccionCrosseling_list"),
	path('create/', prediccionCrosseling_create, name="prediccionCrosseling_create"),
]
