from django.conf.urls import url
from firstapp import views


app_name = 'firstapp'

urlpatterns=[



        url(r'^register/$',views.register,name='register'),
        url(r'^login/$',views.userlogin,name='login'),
        url(r'^error_404/$',views.error_404,name='error_404'),
        url(r'^error_500/$',views.error_500,name='error_500'),

        






]
