from django.urls import path
from . import views

urlpatterns = [
    # ケースカードの価格取得API
    path('api/casecard-price/', views.get_case_card_price, name='get_case_card_price'),
]
