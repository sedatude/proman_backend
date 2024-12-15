"""manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import proman
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import private_files_view



urlpatterns = [
    path('private_files/<path:path>', private_files_view, name='private_files'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('sedaterenadmin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('common/', include('common.urls')),
    path('api/v1/', include('project.urls')),  # Project app'in URL'lerini dahil et

    path('user/', include('userprocess.urls')),
    path('_nested_admin/', include('nested_admin.urls')), 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  
