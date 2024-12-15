from django.urls import path
from . import views

import project

urlpatterns = [

    path('money', views.money, name='money'),
    path('purchasement_type', views.purchasement_type, name='purchasement_type'),
    path('import_purchasement_steps', views.import_purchasement_steps, name='import_purchasement_steps'),
    path('import_purchasement_items', views.import_purchasement_items, name='import_purchasement_items'),


]
 
 