from django.urls import path
from accounts.views import *
from home.views import *

urlpatterns = [
    path('',index,name="index"),
]
