from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('opt-out/<str:urlname>/', views.opt_out, name='opt_out'),
]