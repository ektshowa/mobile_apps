"""mobile_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path('uza_billet/', include('uza_billet.urls', namespace='uza_billet')),
    path('api/', include('rest_api.urls', namespace='rest_api')),
    path('census_api/', include('census_api.urls', namespace='census_api')),
    path('census/', include('census.urls', namespace='census')),
    path('admin/', admin.site.urls),
]
