from django.urls import path
from . import views

import project

from .views import AddProjectLoadDataListView, ProjectListView, ProjectCreateView


urlpatterns = [
    path('projects/add/', ProjectCreateView.as_view(), name='project-add'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/add_project_load_data', AddProjectLoadDataListView.as_view(), name='add_project_load_data'),

    # path('projects/', ProjectListView.as_view(), name='project-list'),
    # path('projects/add/', craete_new_project(), name='project-add'),
    # path('projects/update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    # path('projects/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),
    # path('project-types/', ProjectTypeListView.as_view(), name='project-types'),
    # path('projects/details/<int:project_id>/', ProjectDetailsView.as_view(), name='project-details'),  # Yeni route


]

 
 