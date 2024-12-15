from django.urls import path
from django.urls import path
from .views import ProjectCreateView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    path('projects/add/', ProjectCreateView.as_view(), name='project-add'),
    path('projects/update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    path('projects/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),
]

 
 