from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('main/', views.main, name='main'),
    path('get/<str:element_name>/', views.get, name='get'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.delete, name='delete'),
]
