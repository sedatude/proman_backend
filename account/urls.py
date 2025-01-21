from django.urls import path
from . import views

# from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from .views import RegisterView

# urlpatterns = [
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#   #  path('register/', RegisterView.as_view(), name='register'),
# ]


urlpatterns = [


    path('api/user_info/', views.UserDetailsView.as_view(), name='user_info'),
    path('user_details', views.login, name='api/user_details'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
 

]
 