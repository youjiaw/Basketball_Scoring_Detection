"""bballApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from mainsite.views import login, tracking, compare, history, index, logout
import video_handler.views as vd

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('login/', login),
    path('tracking/', tracking),
    path('compare/<int:no>/', compare, name='compare-url'),
    path('history/', history), 
    path('', index),
    path('logout/', logout),

    path('video/', vd.index),
    path('video/<int:no>/', vd.index, name='vd-url'),
    path('process/', vd.process),
    path('filter/<int:s>/<int:f>/<int:m>/filter_process/', vd.filter_process),
    path('result/', vd.result),
    path('result/<int:edit>/', vd.result),
    path('filter/', vd.filter),
    path('filter/<int:s>/<int:f>/<int:m>/', vd.filter, name='ft-url'),
    path('filter/<int:s>/<int:f>/<int:m>/download/', vd.download),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
