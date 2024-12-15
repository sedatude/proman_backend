from django.urls import path
from . import views


import userprocess

urlpatterns = [

   path('', views.users, name='users'),
   path('new', views.new_user, name='new_user'),
   path('edit_password/<int:id>/', views.edit_password, name='edit_password'),  
   path('edit_rights/<int:id>/', views.edit_rights, name='edit_rights'),  

]
 
 