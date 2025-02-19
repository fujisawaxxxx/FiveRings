from django.db import models
from django.utils import timezone

class OrderHistory(models.Model):
    # 注文番号（5桁、ユニーク）
    order_number = models.CharField(
        max_length=5,
        unique=True,
        verbose_name="注文番号",
        editable=False  # 管理画面での編集を防止
    )

    # 商品基本情報
    PRODUCT_CHOICES = [
        ('consent-color', '同意説明書（カラー）'),
        ('consent-monochrome', '同意説明書（モノクロ）'),
        ('case-card', 'ケースカード（症例報告書）'),
        ('chiken-plan', '治験実施計画書'),
        ('medication-diary', '服薬日誌'),
        ('participation-card', '参加カード'),
    ]
    
    # create_order.htmlの表示順に合わせて定義
    product_type = models.CharField(max_length=50, choices=PRODUCT_CHOICES, verbose_name="商品の種類")
    invoice_detail = models.CharField(max_length=200, blank=True, null=True, verbose_name="詳細請求書名")
    upload_file = models.CharField(max_length=200, blank=True, null=True, verbose_name="入稿ファイル名")
    quantity = models.IntegerField(verbose_name="数量")
    content = models.CharField(max_length=50, blank=True, null=True, verbose_name="本文")
    sanka_card_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="参加カードの種類")
    
    # 複写オプション
    fukusha1 = models.CharField(max_length=50, blank=True, null=True, verbose_name="複写1")
    fukusha2 = models.CharField(max_length=50, blank=True, null=True, verbose_name="複写2")
    fukusha3 = models.CharField(max_length=50, blank=True, null=True, verbose_name="複写3")
    fukusha4 = models.CharField(max_length=50, blank=True, null=True, verbose_name="複写なしミシン目")
    fukusha5 = models.CharField(max_length=50, blank=True, null=True, verbose_name="複写オプション")
    
    # 金額情報
    total_pages = models.CharField(max_length=50, blank=True, null=True, verbose_name="総頁数")
    unit_price = models.IntegerField(verbose_name="単価")
    estimate_result = models.IntegerField(verbose_name="見積もり金額")
    
    # オプション情報
    additional_print = models.BooleanField(default=False, verbose_name="追加（増刷）")
    no_holes = models.BooleanField(default=False, verbose_name="2穴不要")
    remarks = models.TextField(blank=True, null=True, verbose_name="備考")

    # 作成日時
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")

    def save(self, *args, **kwargs):
        if not self.order_number:
            # 最後の注文番号を取得
            last_order = OrderHistory.objects.order_by('-order_number').first()
            if last_order:
                # 最後の注文番号に1を加える
                last_number = int(last_order.order_number)
                new_number = str(last_number + 1).zfill(5)
            else:
                # 最初の注文の場合は00001
                new_number = '00001'
            self.order_number = new_number
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "注文履歴"
        verbose_name_plural = "注文履歴"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.order_number} - {self.get_product_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
