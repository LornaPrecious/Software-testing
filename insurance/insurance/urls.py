"""
URL configuration for insurance project.

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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from useraccounts import views as v
from main import views as mv


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', mv.home, name ='home'),
    path('home/', mv.home, name ='home'), 
    path('contact/', mv.contactUs, name ='contact'),
   
    #path('quote/', v.QuoteFormPreview(QuoteForm)),
  
    path('quote/', v.bradleyForm, name ='quote'),
    #path('preview/', v.add_preview, name ='add_preview'),
    path('register/', v.register, name ='register'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('login/', v.custom_login, name='login'), 
    path('logout/', v.signout, name='signout'), 
    path('activate/<uidb64>/<token>', v.activate, name='activate'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
