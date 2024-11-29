from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # 設定を読み込むため
from django.conf.urls.static import static  # static関数を使用するため
from django.shortcuts import redirect  # リダイレクトを行うために必要

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # 正しい位置に記述されていますか？
    path('items/', include('items.urls')),      # itemsアプリのルーティング

    # ルートURLを /accounts/login/ にリダイレクト
    path('', lambda request: redirect('login')),
]

# メディアファイルの提供を設定 (DEBUG モードのときのみ有効)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
