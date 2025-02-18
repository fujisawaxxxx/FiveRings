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

@login_required
def create_order_view(request):
    # 全てのデータをリクエストから取得
    context = {
        'product_type': request.GET.get('product_type', '選択されていません'),
        'quantity': request.GET.get('quantity', '-'),
        'content': request.GET.get('content', '-'),
        'unit_price': request.GET.get('unit_price', '-'),
        'estimate_result': request.GET.get('estimate_result', '-'),
        'invoice_detail': request.GET.get('invoice_detail', '-'),
        'upload_file': request.GET.get('upload_file', '-'),
        'sanka_card_type': request.GET.get('sanka_card_type', '-'),
        'fukusha1': request.GET.get('fukusha1', '-'),
        'fukusha2': request.GET.get('fukusha2', '-'),
        'fukusha3': request.GET.get('fukusha3', '-'),
        'fukusha4': request.GET.get('fukusha4', '-'),
        'fukusha5': request.GET.get('fukusha5', '-'),
        'total_pages': request.GET.get('total_pages', '-'),
        'additional_print': request.GET.get('additional_print', 'false'),
        'no_holes': request.GET.get('no_holes', 'false'),
        'remarks': request.GET.get('remarks', '-'),
    }

    return render(request, 'accounts/create_order.html', context)