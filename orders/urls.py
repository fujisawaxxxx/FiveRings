# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 同意説明書の価格取得API
    path('api/agree-color/', views.get_agree_color, name='get_agree_color'),
    # 同意説明書の価格取得API
    path('api/agree-monochrome/', views.get_agree_monochrome, name='get_agree_monochrome'),
    # ケースカードの価格取得API
    path('api/casecard-price/', views.get_case_card_price, name='get_case_card_price'),
    # 治験実施計画書の価格取得API
    path('api/chiken-plan-price/', views.get_chiken_plan_price, name='get_chiken_plan_price'),
    # 服薬日誌の価格取得API
    path('api/medication-diary-price/', views.get_medication_diary_price, name='get_medication_diary_price'),
]
