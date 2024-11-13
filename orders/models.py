# models.py
from django.db import models

class AgreementColor(models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "同意説明書（カラー）"
        verbose_name_plural = "同意説明書（カラー）"

class AgreementMonochrome (models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "同意説明書（モノクロ）"
        verbose_name_plural = "同意説明書（モノクロ）"

class CaseCard (models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "ケースカード（症例報告書）"
        verbose_name_plural = "ケースカード（症例報告書）"

class Chiken (models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "治験実施計画書"
        verbose_name_plural = "治験実施計画書"

class Fukuyaku (models.Model):
    number_of_sheets = models.IntegerField(verbose_name="枚数")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="単価")

    def __str__(self):
        return f"{self.number_of_sheets}枚 - {self.unit_price}円"

    class Meta:
        verbose_name = "服薬日誌"
        verbose_name_plural = "服薬日誌"

