from django.conf.urls import url
from first_app import views

app_name = 'first_app'

urlpatterns = [
    url(r'^$', views.firstappindex, name='firstappindex'),
    url(r'^help', views.help, name='help'),
    url(r'^other/$', views.other, name='other'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'special/', views.special, name='special'),
]