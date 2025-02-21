# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import ParticipationCard  # 追加
from order_rireki.models import OrderHistory  # 追加
from django.contrib import messages  # 追加
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

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
    if request.method == 'POST':
        try:
            order = OrderHistory.objects.create(
                staff=request.user,
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

            # 管理者のメールアドレスを取得
            admin_email = User.objects.get(username='admin').email

            # メール本文を作成
            mail_body = f"""
新しい注文が入りました。

注文番号: {order.order_number}
担当者: {order.staff}
作成日時: {order.created_at}
商品種類: {order.product_type}
請求先: {order.invoice_detail}
アップロードファイル: {order.upload_file}
数量: {order.quantity}
内容: {order.content}
参加カード種類: {order.sanka_card_type}
複写1: {order.fukusha1}
複写2: {order.fukusha2}
複写3: {order.fukusha3}
複写4: {order.fukusha4}
複写5: {order.fukusha5}
総ページ数: {order.total_pages}
単価: {order.unit_price}
見積金額: {order.estimate_result}
追加印刷: {'あり' if order.additional_print else 'なし'}
穴なし: {'あり' if order.no_holes else 'なし'}
備考: {order.remarks}

管理画面URL: http://サイトのドメイン/admin/order_rireki/orderhistory/{order.id}/
            """

            # メール送信
            send_mail(
                subject=f'新規注文通知 - 注文番号: {order.order_number}',
                message=mail_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[admin_email],
                fail_silently=False,
            )

            # 既存の処理を継続
            context = {
                'success_message': f'注文番号 {order.order_number} で発注が完了しました。',
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
        except Exception as e:
            messages.error(request, f'発注処理中にエラーが発生しました: {str(e)}')
    
    # 通常の表示処理
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