from django.urls import path
from .views import UserAccessToken
from django.views.decorators.csrf import csrf_exempt
urlpatterns =[
path('usertoken/',csrf_exempt(UserAccessToken.as_view()))
]
