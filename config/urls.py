from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # リダイレクトを行うために必要

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # 正しい位置に記述されていますか？
    path('orders/', include('orders.urls')),      # ordersアプリのルーティング

    path('', lambda request: redirect('login')),  # ルートURLを /accounts/login/ にリダイレクト
]
