from django.urls import path

from . import views

urlpatterns = [
    path('write/', views.write, name='write'),
    path('inbox/', views.inbox, name='inbox'),
    path('unread/', views.unread, name='unread'),
    path('sent/', views.sent, name='sent'),
    path('read/', views.read, name='read'),
    path('delete/', views.delete, name='delete'),
]
