# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import ParticipationCard  # 追加
from order_rireki.models import OrderHistory  # 追加
from django.contrib import messages  # 追加

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
    if request.method == 'POST':  # 発注依頼ボタンが押された場合
        try:
            # OrderHistoryモデルにデータを保存
            order = OrderHistory.objects.create(
                product_type=request.GET.get('product_type', ''),
                invoice_detail=request.GET.get('invoice_detail', ''),
                upload_file=request.GET.get('upload_file', ''),
                quantity=int(request.GET.get('quantity', 0)),
                content=request.GET.get('content', ''),
                sanka_card_type=request.GET.get('sanka_card_type', ''),
                fukusha1=request.GET.get('fukusha1', ''),
                fukusha2=request.GET.get('fukusha2', ''),
                fukusha3=request.GET.get('fukusha3', ''),
                fukusha4=request.GET.get('fukusha4', ''),
                fukusha5=request.GET.get('fukusha5', ''),
                total_pages=request.GET.get('total_pages', ''),
                unit_price=int(request.GET.get('unit_price', 0)),
                estimate_result=int(request.GET.get('estimate_result', 0)),
                additional_print=request.GET.get('additional_print', 'false') == 'true',
                no_holes=request.GET.get('no_holes', 'false') == 'true',
                remarks=request.GET.get('remarks', '')
            )
            messages.success(request, f'注文番号 {order.order_number} で発注が完了しました。')
            return redirect('main')  # メイン画面にリダイレクト
        except Exception as e:
            messages.error(request, f'発注処理中にエラーが発生しました: {str(e)}')
            
    # GETリクエストの場合は通常の処理
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