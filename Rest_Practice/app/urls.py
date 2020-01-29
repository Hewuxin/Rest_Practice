from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^users/$', views.UsersAPIView.as_view()),
    url(r'^users/(?P<pk>\d+)/$', views.UserAPIView.as_view(), name='user-detail'),
    url(r'^address/$', views.AddressesViewSet.as_view(
        {'get': 'list',
         'post': 'create'})),
    url(r'^address/(?P<pk>\d+)/$', views.AddressesViewSet.as_view(
        {'get': 'retrieve'}
    ), name='address-detail'),
]

