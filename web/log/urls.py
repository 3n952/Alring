from django.urls import path
from .views import *

urlpatterns = [
    path('log/',log , name = 'log'),
]