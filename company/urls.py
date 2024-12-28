from django.urls import path
from . import views

import company

urlpatterns = [

    path('new_project', views.new_project, name='new_project'),
   
]
 
 