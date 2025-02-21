# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import ParticipationCard  # 追加
from order_rireki.models import OrderHistory  # 追加
from django.contrib import messages  # 追加
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.conf import settings
import os
from datetime import datetime
from django.http import JsonResponse

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
            # 商品種類を取得
            product_type = request.GET.get('product_type', '')
            
            # 同意説明書の場合とそれ以外で分岐
            if product_type in ['consent-color', 'consent-monochrome']:
                # 同意説明書の場合は通常通りの値を使用
                fukusha_values = {
                    'fukusha1': request.GET.get('fukusha1', ''),
                    'fukusha2': request.GET.get('fukusha2', ''),
                    'fukusha3': request.GET.get('fukusha3', ''),
                    'fukusha4': request.GET.get('fukusha4', ''),
                    'fukusha5': request.GET.get('fukusha5', ''),
                }
            else:
                # 同意説明書以外の場合は全て'-'を設定
                fukusha_values = {
                    'fukusha1': '-',
                    'fukusha2': '-',
                    'fukusha3': '-',
                    'fukusha4': '-',
                    'fukusha5': '-',
                }

            # OrderHistoryオブジェクトの作成
            order = OrderHistory.objects.create(
                staff=request.user,
                product_type=product_type,
                invoice_detail=request.GET.get('invoice_detail', ''),
                upload_file=request.GET.get('upload_file', ''),
                quantity=int(request.GET.get('quantity', 0)),
                content=request.GET.get('content', ''),
                sanka_card_type=request.GET.get('sanka_card_type', ''),
                # 複写関連の値を設定
                fukusha1=fukusha_values['fukusha1'],
                fukusha2=fukusha_values['fukusha2'],
                fukusha3=fukusha_values['fukusha3'],
                fukusha4=fukusha_values['fukusha4'],
                fukusha5=fukusha_values['fukusha5'],
                total_pages=request.GET.get('total_pages', ''),
                unit_price=int(request.GET.get('unit_price', 0)),
                estimate_result=int(request.GET.get('estimate_result', 0)),
                additional_print=request.GET.get('additional_print', 'false') == 'true',
                no_holes=request.GET.get('no_holes', 'false') == 'true',
                remarks=request.GET.get('remarks', '')
            )

            # 管理者のメールアドレスを取得
            admin_email = User.objects.get(username='admin').email

            # 商品種類の日本語変換用の辞書
            product_type_dict = {
                'consent-color': '同意説明書（カラー）',
                'consent-monochrome': '同意説明書（モノクロ）',
                'case-card': 'ケースカード（症例報告書）',
                'chiken-plan': '治験実施計画書',
                'medication-diary': '服薬日誌',
                'participation-card': '参加カード'
            }

            # 商品種類を日本語に変換
            product_type_ja = product_type_dict.get(order.product_type, order.product_type)

            # 同意説明書の場合のみ複写関連の情報を表示
            if order.product_type in ['consent-color', 'consent-monochrome']:
                copy_info = f"""
            複写1: {order.fukusha1}
            複写2: {order.fukusha2}
            複写3: {order.fukusha3}
            複写なしミシン目: {order.fukusha4}
            複写オプション: {order.fukusha5}"""
            else:
                copy_info = """
            複写1: -
            複写2: -
            複写3: -
            複写なしミシン目: -
            複写オプション: -"""

            # メール本文用の項目を準備（値が'-'の場合はNoneを設定）
            mail_items = {
                '注文番号': order.order_number,
                '担当者': order.staff,
                '作成日時': order.created_at,
                '商品種類': product_type_ja,
                '詳細請求書名': order.invoice_detail if order.invoice_detail != '-' else None,
                'アップロードファイル': order.upload_file if order.upload_file != '-' else None,
                '数量': order.quantity,
                '本文': f"{order.content}頁" if order.content != '-' else None,
                '参加カード種類': order.sanka_card_type if order.sanka_card_type != '-' else None,
                '複写1': order.fukusha1 if order.fukusha1 != '-' else None,
                '複写2': order.fukusha2 if order.fukusha2 != '-' else None,
                '複写3': order.fukusha3 if order.fukusha3 != '-' else None,
                '複写なしミシン目': order.fukusha4 if order.fukusha4 != '-' else None,
                '複写オプション': order.fukusha5 if order.fukusha5 != '-' else None,
                '総ページ数': f"{order.total_pages}頁" if order.total_pages != '-' else None,
                '単価': f"{order.unit_price}円",
                '見積金額': f"{order.estimate_result}円",
                '追加（増刷）': 'あり' if order.additional_print else None,
                '２穴': '不要' if order.no_holes else None,
                '備考': order.remarks if order.remarks != '-' else None,
            }

            # 管理者向けメール本文の作成
            admin_mail_body = "新しい注文が入りました。\n\n"
            for key, value in mail_items.items():
                if value is not None:  # 値が None でない場合のみ追加
                    admin_mail_body += f"{key}: {value}\n"
            
            admin_mail_body += f"\n管理画面URL: http://127.0.0.1:8000//admin/order_rireki/orderhistory/{order.id}/"

            # 管理者へのメール送信
            email = EmailMessage(
                subject=f'ファイブリングス新規注文通知 - 注文番号: {order.order_number}',
                body=admin_mail_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[admin_email],
            )

            # アップロードされたファイルを添付
            if order.upload_file and order.upload_file != '-':
                file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', order.upload_file)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        email.attach(order.upload_file, f.read(), 'application/octet-stream')

            email.send(fail_silently=False)

            # ユーザー向けメール本文の作成
            user_mail_body = f"{request.user.username} 様\n\n"
            for key, value in mail_items.items():
                if value is not None:  # 値が None でない場合のみ追加
                    user_mail_body += f"{key}: {value}\n"

            # ユーザーへのメール送信
            user_email = EmailMessage(
                subject=f'【注文受付完了 {order.order_number}】ご注文ありがとうございます',
                body=user_mail_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[request.user.email],
            )
            user_email.send(fail_silently=False)

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

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # ファイル名とタイムスタンプを結合
        filename, ext = os.path.splitext(uploaded_file.name)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{filename}_{timestamp}{ext}"
        
        # アップロード先のパスを作成
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # ファイルを保存
        file_path = os.path.join(upload_dir, new_filename)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        return JsonResponse({
            'success': True,
            'filename': new_filename
        })
    
    return JsonResponse({'success': False}, status=400)