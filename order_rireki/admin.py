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
        'invoice_detail',
        'quantity',
        'estimate_result',
        'yamato_number',  # ヤマト伝票番号を表示に追加
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
    # ... 他の設定 ...
