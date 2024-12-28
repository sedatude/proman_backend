from django.urls import path

from .views import ProjectCreateView, ProjectDetailsView, ProjectUpdateView, ProjectDeleteView, ProjectListView
from .views import ProjectTypeListView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/add/', ProjectCreateView.as_view(), name='project-add'),
    path('projects/update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    path('projects/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),
    path('project-types/', ProjectTypeListView.as_view(), name='project-types'),
    path('projects/details/<int:project_id>/', ProjectDetailsView.as_view(), name='project-details'),  # Yeni route


]

 
 