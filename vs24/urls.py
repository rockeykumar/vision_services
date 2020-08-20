from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.signup, name='signup'),
    path('font_test/', views.font_test, name='font_test'),
    path('product/add/', views.insert_product_database, name='insert_product_database'),
    path('product/add/seller/', views.add_product_seller, name='add_product_seller'),
    path('product/add/seller/detail', views.add_product_detail, name='add_product_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
