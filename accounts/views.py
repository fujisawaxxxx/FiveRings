# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import ParticipationCard  # 追加

@login_required  # ログインが必要なビューとして設定
def main_view(request):
    # 管理画面で登録された参加カードの種類を取得
    participation_cards = ParticipationCard.objects.all().values_list('cardtype', flat=True)
    
    context = {
        'participation_cards': participation_cards,
    }
    return render(request, 'accounts/main.html', context)

@login_required  # 注文書作成画面へのビュー
def create_order_view(request):
    # 入力データをリクエストから取得
    product_type = request.GET.get('product_type', '選択されていません')
    quantity = request.GET.get('quantity', '-')
    content = request.GET.get('content', '-')
    unit_price = request.GET.get('unit_price', '-')
    estimate_result = request.GET.get('estimate_result', '-')

    context = {
        'product_type': product_type,
        'quantity': quantity,
        'content': content,
        'unit_price': unit_price,
        'estimate_result': estimate_result,
    }

    return render(request, 'accounts/create_order.html', context)