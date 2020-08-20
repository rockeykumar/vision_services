from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<slug:slug>/', views.index, name='index'),
    path('', views.dynamic_categories, name='dynamic_categories'),
    path('<str:name>/<slug:slug>/', views.index, name='index'),
]
