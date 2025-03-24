from django.contrib import admin
from .models import OrderHistory

# Register your models here.

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'staff',  # 担当者を表示に追加
        'created_at',
        'product_type',
        'project_name',
        'invoice_detail',
        'quantity',
        'estimate_result',
        'upload_file',  # 入稿ファイル名を表示に追加
        'delivery_date',  # 納期を表示に追加
    )

    list_filter = (
        'staff',  # 担当者でフィルタリングできるように追加
        'product_type',
        'created_at',
        'additional_print',
        'no_holes',
        'delivery_date',  # 納期でフィルタリングできるように追加
    )
    
    # タイムスタンプ付きのファイル名を詳細画面で非表示にする
    exclude = ('upload_file_timestamped',)
    # ... 他の設定 ...
