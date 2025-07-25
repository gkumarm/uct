"""uct URL Configuration

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
from django.urls import path, include, re_path
#from django.conf.urls import handler400, handler403, handler404, handler500

#from uauth.views import logout, home, error_404, error_500

#handler400 = 'uct.views.error_400'
#handler403 = 'uct.views.error_403'
# handler404 = 'uauth.views.error_404'
# handler500 = 'uauth.views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include("uauth.urls")),
    path('', include('todo.urls')),
]