from django.urls import path
from . import views

app_name='cit2020'
urlpatterns = [
    path('', views.index, name='index'),
    path('answer/', views.answer , name='answer'),
    path('lboard/', views.lboard , name='lboard'),
    path('rules/', views.rules , name='rules'),
]
