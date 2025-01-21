from django.urls import path

from .views import (
    PurchasementDetailUpdateView, PurchasementStepDetailUpdateView, 
    PurchasementListView, PurchasementDetailView, PurchasementTemplateUpdateView
)


urlpatterns = [
    path('purchasement/<int:project_id>/', PurchasementListView.as_view(), name='project-list'),
    path('purchasement_details', PurchasementDetailView.as_view(), name='purchasement_details'),
    path('purchasement/update/', PurchasementStepDetailUpdateView.as_view(), name='purchasement_update'),
    path('purchasement/update_template/', PurchasementTemplateUpdateView.as_view(), name='purchasement_update_template'),
    path('purchasement_details/update/', PurchasementDetailUpdateView.as_view(), name='purchasement_details'),

    # path('projects/', ProjectListView.as_view(), name='project-list'),
    # path('projects/add/', craete_new_project(), name='project-add'),
    # path('projects/update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    # path('projects/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),
    # path('project-types/', ProjectTypeListView.as_view(), name='project-types'),
    # path('projects/details/<int:project_id>/', ProjectDetailsView.as_view(), name='project-details'),  # Yeni route


]

 
 