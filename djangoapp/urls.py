from django.urls import path
from . import views





urlpatterns = [
    path('login/', views.loginpage, name='login'),
     path('logout/', views.logoutpage, name='logout'),
    path('RegisterPage/', views.RegisterPage, name='RegisterPage'),

    path('', views.home, name='home'),
    path('room/<int:pk>/', views.Rooms, name='Rooms'),

    path('userprofile/<int:pk>', views.userprofile, name='userprofile'),


    path('form_room/', views.createRoom, name='createRoom'),
    path('form_room/<int:pk>', views.updateroom, name='updateroom'),
    path('deleteroom/<int:pk>', views.deleteroom, name='deleteroom'),

    path('deletemessage/<int:pk>', views.deletemessage, name='deletemessage')
]