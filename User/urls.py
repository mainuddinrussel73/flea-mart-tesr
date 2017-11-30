from django.conf.urls import url
from User import views
from django.contrib import admin
from .views import (
    PostLikeAPIToggle,

    )


app_name = 'User'

urlpatterns=[
        url(r'^home/$',views.userhome,name='home'),
        url(r'^(?P<slug>[\w-]+)likesupdate/$',views.Likesupdate,name='likesupdate'),
        url(r'^(?P<slug>[\w-]+)details/$',views.showitem,name='details'),
        url(r'^(?P<slug>[\w-]+)delete/$',views.deleteitem,name='delete'),
        url(r'^auctions/$',views.auctions,name='auctions'),
        url(r'^(?P<slug>[\w-]+)bid/$',views.bid,name='bid'),
        url(r'^bids/$',views.bids,name='bids'),
        url(r'^check/$',views.check,name='check'),
        
        # url(r'^(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
        url(r'^api/(?P<slug>[\w-]+)/likes/$',PostLikeAPIToggle.as_view(),name='likes-api-toggle'),
        url(r'^profile/$',views.userprofile,name='profile'),
        url(r'^sellitem/$',views.sellitem,name='sellitem'),
        url(r'^post/$', views.Post, name='post'),
        url(r'^comment/$', views.Comment, name='comment'),
        url(r'^notification/$', views.Notifications, name='notification'),
        url(r'^messages/$', views.Messages, name='messages'),



]
