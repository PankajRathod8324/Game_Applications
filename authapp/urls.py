from django.urls import path
from authapp import views
from authapp.views import *

urlpatterns = [
    path('', views.Home, name="Home"),
    path('signup', views.signup, name="signup"),
    path('login', views.handlelogin, name="handlelogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('contact', views.contact, name="contact"),
    path('join', views.enroll, name='enroll'),
    path('profile', views.profile, name='profile'),
    path('gallery', views.gallery, name='gallery'),
    path('attendance', views.attendance, name='attendance'),
    path('ForgetPassword', views.ForgetPassword, name='ForgetPassword'),
    path('change_password/<uid64>/<token>/',
         views.ChangePassword, name="change_password"),
    
    path('add_equipment',views.Add_Equipment,name='add_equipment'),
    path('view_equipment',views.View_Equipment,name='view_equipment'),
    path('delete_equipment(?p<int:pid>)', views.Delete_Equipment, name='delete_equipment'),
    path('video', views.Videos, name='video'),
    # path('payment', views.payment, name='payment'),

]
