from django.urls import path
from . import views


   

urlpatterns = [
    path('', views.index, name='index' ),
    path('movie/<str:uu_id>/', views.movie, name='movie' ),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup' ),
    path('logout/', views.logout, name='logout'),
    path('add_to_list/', views.add_to_list, name='add-to-list'),
    path('my-list/', views.my_list, name='my-list'),
    path('search', views.search, name='search'),
   path('genre/<str:genre>/', views.genre, name='genre'),
]