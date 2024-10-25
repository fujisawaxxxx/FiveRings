from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # 正しい位置に記述されていますか？
    path('orders/', include('orders.urls')),      # ordersアプリのルーティング
]
