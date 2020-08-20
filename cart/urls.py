from django.urls import path
from .import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cart, name='cart'),
    path('cart_list_views/', views.cart_list_views, name='cart_list_views'),
    path('ajax_dynamical/', views.ajax_dynamical, name='ajax_dynamical'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('order-Place/', views.order_Place, name='order-Place'),
    path('confirmOrder/', views.confirmOrder, name='confirmOrder'),

    path('cart_list_views/<str:name>/<slug:slug>/', views.index, name='index'),         # 06-04-2020
    path('handlerequest/', views.handlerequest, name='HandleRequest'),                   # 07-04-2020
]
