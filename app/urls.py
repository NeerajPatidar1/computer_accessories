from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm , MyPasswordChangeForm, MyPasswordResetForm,  MysetPasswordForm
from django.contrib.auth.models import User
urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),   
    path('buy_one_product',views.buy_single_pro,name='buy_one_product'),
    path('single_pro_price',views.single_pro_price,name='single_pro_price'),
    path('payment_single_item',views.payment_single_item,name='payment_single_item'),
    path('callback1',views.callback1,name='callback1'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('callback/', views.callback, name='callback'),
    path('buy_single',views.initiate_payment_for_single,name='buy_single')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
