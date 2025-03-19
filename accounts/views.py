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
from django.core.files.storage import FileSystemStorage
import time
from django.utils import timezone
from project_name.models import Project

@login_required  # ログインが必要なビューとして設定
def main_view(request):
    # 管理画面で登録された参加カードの種類を取得
    participation_cards = ParticipationCard.objects.all().values_list('cardtype', flat=True)
    
    # プロジェクト一覧を取得
    projects = Project.objects.all().values_list('project_name', flat=True)
    
    context = {
        'participation_cards': participation_cards,
        'projects': projects,  # プロジェクト一覧をコンテキストに追加
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

            # アップロードファイル情報を取得
            upload_file = request.GET.get('upload_file', '')
            # タイムスタンプ付きのファイル名を取得
            upload_file_timestamped = request.GET.get('upload_file_timestamped', '')
            # 施設名を取得
            facility = request.GET.get('facility', '')

            # OrderHistoryオブジェクトの作成
            order = OrderHistory.objects.create(
                staff=request.user,
                product_type=product_type,
                invoice_detail=request.GET.get('invoice_detail', ''),
                upload_file=upload_file,
                upload_file_timestamped=upload_file_timestamped,  # タイムスタンプ付きファイル名を保存
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
                remarks=request.GET.get('remarks', ''),
                facility=facility,  # 施設名を保存
                project_name=request.GET.get('project_name', ''),  # プロジェクト名を保存
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
                'participation-card': '参加カード',
                'generic': '汎用',  # 汎用商品タイプの表示名を追加
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
                '商品種類': product_type_ja,
                '詳細請求書名': order.invoice_detail if order.invoice_detail != '-' else None,
                'アップロードファイル': order.upload_file if order.upload_file != '-' else None,
                '施設名': order.facility if order.facility else None,
                'プロジェクト名': order.project_name if order.project_name != '-' else None,
                '数量': order.quantity,
                '本文': f"{order.content}頁" if order.content != '-' else None,
                '参加カード種類': order.sanka_card_type if order.sanka_card_type != '-' else None,
                '複写1': order.fukusha1 if order.fukusha1 != '-' else None,
                '複写2': order.fukusha2 if order.fukusha2 != '-' else None,
                '複写3': order.fukusha3 if order.fukusha3 != '-' else None,
                '複写なしミシン目': order.fukusha4 if order.fukusha4 != '-' else None,
                '複写オプション': order.fukusha5 if order.fukusha5 != '-' else None,
                '総ページ数': f"{order.total_pages}頁" if order.total_pages != '-' else None,
                '単価': f"{order.unit_price:,}円",
                '見積金額': f"{order.estimate_result:,}円",
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
                file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', order.upload_file_timestamped)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        email.attach(order.upload_file, f.read(), 'application/octet-stream')

            email.send(fail_silently=False)

            # ユーザー向けメール本文の作成
            user_mail_body = f"{request.user.username} 様\n\n以下の内容でご注文を受け付けました。\n\n"
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
                'unit_price': f"{int(request.GET.get('unit_price', 0)):,}",
                'estimate_result': f"{int(request.GET.get('estimate_result', 0)):,}",
                'invoice_detail': request.GET.get('invoice_detail', '-'),
                'upload_file': request.GET.get('upload_file', '-'),
                'facility': request.GET.get('facility', '-'),
                'project_name': request.GET.get('project_name', '-'),
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
    unit_price = request.GET.get('unit_price', '-')
    estimate_result = request.GET.get('estimate_result', '-')
    
    # 数値の場合はカンマ区切りに変換
    if unit_price != '-' and unit_price.isdigit():
        unit_price = f"{int(unit_price):,}"
    
    if estimate_result != '-' and estimate_result.isdigit():
        estimate_result = f"{int(estimate_result):,}"
    
    context = {
        'product_type': request.GET.get('product_type', '選択されていません'),
        'quantity': request.GET.get('quantity', '-'),
        'content': request.GET.get('content', '-'),
        'unit_price': unit_price,
        'estimate_result': estimate_result,
        'invoice_detail': request.GET.get('invoice_detail', '-'),
        'upload_file': request.GET.get('upload_file', '-'),
        'facility': request.GET.get('facility', '-'),
        'project_name': request.GET.get('project_name', '-'),
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
        
        # オリジナルのファイル名を保存
        original_filename = uploaded_file.name
        
        # ファイル名と拡張子を分離
        filename, file_extension = os.path.splitext(original_filename)
        
        # 現在の日時をyyyymmddhhmmss形式で取得
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        
        # タイムスタンプ付きのファイル名を生成（保存用）
        # 形式: 元のファイル名_yyyymmddhhmmss.拡張子
        timestamped_filename = f"{filename}_{timestamp}{file_extension}"
        
        # uploads ディレクトリを指定してファイルを保存
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        saved_filename = fs.save(timestamped_filename, uploaded_file)
        
        # 成功レスポンスを返す（オリジナルのファイル名とタイムスタンプ付きファイル名の両方を含める）
        return JsonResponse({
            'success': True, 
            'original_filename': original_filename,  # 表示用のオリジナルファイル名
            'timestamped_filename': saved_filename,  # 保存用のタイムスタンプ付きファイル名
        })
    
    return JsonResponse({'success': False})

def get_product_type_display(product_type):
    product_types = {
        'consent-color': '同意説明書（カラー）',
        'consent-monochrome': '同意説明書（モノクロ）',
        'case-card': 'ケースカード（症例報告書）',
        'chiken-plan': '治験実施計画書',
        'medication-diary': '服薬日誌',
        'participation-card': '参加カード',
        'generic': '汎用',  # 汎用商品タイプの表示名を追加
    }
    return product_types.get(product_type, product_type)

@login_required
def get_order_data(request, order_number):
    try:
        # 注文番号から注文履歴を検索
        order = OrderHistory.objects.get(order_number=order_number)
        
        # 商品タイプIDを取得（HTMLのプルダウンで選択される値）
        product_type_map = {
            '同意説明書（カラー）': 'consent-color',
            '同意説明書（モノクロ）': 'consent-monochrome',
            'ケースカード（症例報告書）': 'case-card',
            '治験実施計画書': 'chiken-plan',
            '服薬日誌': 'medication-diary',
            '参加カード': 'participation-card',
            '汎用': 'generic',
        }
        
        # データベースの値をフロントエンドの値に変換
        # product_typeは保存されている値（同意説明書（カラー）など）
        # ドロップダウンの値（consent-colorなど）に変換
        product_type_display = get_product_type_display(order.product_type)
        product_type_id = product_type_map.get(product_type_display, order.product_type)
        
        # レスポンスデータの作成
        data = {
            'success': True,
            'data': {
                'invoice_detail': order.invoice_detail or '',
                'facility': order.facility or '',
                'project_name': order.project_name or '',
                'product_type': product_type_id,
                'quantity': order.quantity,
                'content': order.content,
                'sanka_card_type': order.sanka_card_type or '',
                'no_holes': order.no_holes,
                # 必要に応じて他のフィールドを追加
            }
        }
        
        return JsonResponse(data)
    
    except OrderHistory.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '指定された注文番号のデータが見つかりませんでした'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'データ取得エラー: {str(e)}'
        })