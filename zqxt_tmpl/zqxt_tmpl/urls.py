"""zqxt_tmpl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from learn import views as learn_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^index$',learn_views.index,name='index'),
    url(r'^about$',learn_views.about,name='about'),
    url(r'^features$',learn_views.features,name='features'),
    url(r'^work$',learn_views.work,name='work'),
    url(r'^contact$',learn_views.contact,name='contact'),
    url(r'^login$',learn_views.login,name='login'),
    url(r'^Register$',learn_views.Register,name='Register'),
    url(r'^forget$',learn_views.forget,name='forget'),
    url(r'^jump$',learn_views.jump,name='jump'),
    url(r'^logout$',learn_views.logout,name='logout'),
    url(r'^person_info',learn_views.info,name='info'),
    url(r'^change_password',learn_views.cdpwd,name='cdpwd'),
    url(r'^info_confirm',learn_views.info_confirm,name='info_confirm'),
    url(r'^qr_code_create_dushsdfuihsd$', learn_views.qr_code, name='qr_code'),
    # url(r'^findback$', learn_views.findback, name='findback'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)