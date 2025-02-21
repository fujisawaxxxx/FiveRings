from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # リダイレクトを行うために必要
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # 正しい位置に記述されていますか？
    path('items/', include('items.urls')),      # itemsアプリのルーティング

    path('', lambda request: redirect('login')),  # ルートURLを /accounts/login/ にリダイレクト
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
