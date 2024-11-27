# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('main/', views.main_view, name='main'),  # メイン画面へのURL
    path('create_order/', views.create_order_view, name='create_order'),  # 注文確認画面へのURL

]
