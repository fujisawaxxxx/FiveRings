from django.contrib import admin
from .models import OrderHistory

# Register your models here.

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',  # 注文番号を先頭に追加
        'created_at',
        'product_type',
        'invoice_detail',
        'quantity',
        'estimate_result',
        'additional_print',
    )
    # ... 他の設定 ...
