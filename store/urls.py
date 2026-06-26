from django.contrib import admin
from django.urls import path, include
from store import views  # or shop/views depending on your app name
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # 👈 Default page when server starts
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('buynow/', views.buynow, name='buynow'), 
    path('payment/', views.payment_view, name='payment'),
    path('cart/', views.cart_view, name='cart'),
    path('admin_login/', views.admin_login, name='admin_login'),   
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_home/add_product/', views.add_product, name='add_product'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path("payment/<int:id>/", views.payment, name="payment"),
    path('admin_home/orders/', views.admin_orders, name='admin_orders'),




    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
