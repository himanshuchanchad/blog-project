"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.log_out,name='logout'),
    path('detail/',views.detail,name='detail'),
    path('changepass/',views.changepass,name='changepass'),
    path('cb/',views.createblog,name='cb'),
    path('blog/<slug:title>/',views.detailblog,name='blogdetail'),
    path('dp/',views.dispblog,name='display')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
