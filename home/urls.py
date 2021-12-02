from django.urls import path
from . import views

urlpatterns=[
    path('',views.main,name='main'),
    path('buy',views.buy_1,name='buy_1'),
    path('buy2',views.buy_2,name='buy2'),
    path('buy3',views.buy_3,name='buy2'),
    path('cars', views.cars, name='cars'),
    path('topics', views.topics, name='topics'),
    path('about', views.about, name='about'),
    path('index',views.index,name='index'),
    path('sell/',views.sell1,name='sell'),
    path('login/', views.login, name='login'),
    path('login/signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
]