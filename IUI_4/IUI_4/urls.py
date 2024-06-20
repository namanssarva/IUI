"""
URL configuration for IUI_4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from Klasur_mama.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Klasur_mama import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path("",views.home, name="home"),
    path('login/',views.login,name="login"),
    path('about/',views.about,name="about"),
    path('register/',views.register, name ="register"),
    
    path('upload/', views.upload_document, name='upload_document'),
    path('process/<int:document_id>/', views.process_document, name='process_document'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()