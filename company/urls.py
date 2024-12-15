from django.urls import path
from . import views


import company

urlpatterns = [

    # path('', views.dashboard, name='dashboard'),
    # path('mydash', views.mydash, name='mydash'),
    # path('new_company/', views.new_company, name='new_company'),
    # path('open_company/', views.open_company, name='open_company'),
    path('delete_company/', views.delete_company, name='delete_company'),
    path('edit_company/<int:id>/', views.edit_company, name='edit_company'),
    
    path('save_selling_company_manuel/', views.save_selling_company_manuel, name='save_selling_company_manuel'),#work with last list
    path('save_product_manuel/', views.save_product_manuel, name='save_product_manuel'),#work with last list
    path('save_materials_manual/', views.save_materials_manual, name='save_materials_manual'),#work with last list
    path('add_new_info/', views.add_new_info, name='add_new_info'),#work with last list

    path('save_product_materials/', views.save_product_materials, name='save_product_materials'),#reçete
    path('save_product_material_new/', views.save_product_material_new, name='save_product_material_new'),
    path('create_product_materials/', views.create_product_materials, name='create_product_materials'),
    path('new_company/', views.new_company, name='new_company'),
    path('purchasing/', views.purchasing, name='purchasing'),
    path('logistic/', views.logistic, name='logistic'),
    path('distributor/', views.distributor, name='distributor'),
     
    path('company_processes', views.company_processes, name='company_processes'),
    path('moneyrate/', views.moneyrate, name='moneyrate'),
    
  #  path('view_pdf/<str:path>', views.view_pdf, name='view_pdf'),

]
 
 