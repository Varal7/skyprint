from django.conf.urls import url
from . import views


urlpatterns = [
        url(r'^home$', views.home, name='home'),
        url(r'^input$', views.input, name='input'),
        url(r'^all', views.all, name='all'),
        url(r'^test', views.test, name='test'),
        url(r'', views.home, name='home'),
        ]
