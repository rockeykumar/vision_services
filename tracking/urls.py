from django.urls import path
from .import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.__tracking__, name='tracking'),
    path('<int:id>', views.__orderStatus__, name='orderStatus'),
    path('orderCancel/', views.__orderCancel__, name='order-cancel'),
    path('orderCancel/', views.index, name='index'),
    path('<str:name>/<slug:slug>/', views.index, name='index'),
]
