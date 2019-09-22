from django.urls import path
from .import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('product-detail-views/', views.product_detail_views, name='product-detail-views'),
    path('cart/', views.cart, name='cart'),
]
