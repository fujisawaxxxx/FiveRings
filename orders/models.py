from django.db import models

class AgreementColor(models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "同意説明書カラー"
        verbose_name_plural = "同意説明書カラー"

class AgreementMonochrome (models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "同意説明書モノクロ"
        verbose_name_plural = "同意説明書モノクロ"

class CaseCard (models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "ケースカード"
        verbose_name_plural = "ケースカード"

class Chiken (models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "治験計画書"
        verbose_name_plural = "治験計画書"

