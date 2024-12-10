# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime  
import os

@login_required  # ログインが必要なビューとして設定
def main_view(request):
    return render(request, 'accounts/main.html')

@login_required  # 注文書作成画面へのビュー
def create_order_view(request):
    # 入力データをリクエストから取得
    product_type = request.GET.get('product_type', '選択されていません')
    quantity = request.GET.get('quantity', '-')
    content = request.GET.get('content', '-')
    unit_price = request.GET.get('unit_price', '-')
    estimate_result = request.GET.get('estimate_result', '-')
    # 添付ファイル名を取得
    attached_file = request.GET.get('attached_file', '-')
    original_filename = request.GET.get('original_filename', '-')  # 追加
    
    context = {
        'product_type': product_type,
        'quantity': quantity,
        'content': content,
        'unit_price': unit_price,
        'estimate_result': estimate_result,
        'attached_file': attached_file,  # コンテキストに添付ファイル情報を追加
        'original_filename': original_filename,  # 追加
        'MEDIA_URL': settings.MEDIA_URL,  # メディアURLを追加
    }

    return render(request, 'accounts/create_order.html', context)


@login_required
def upload_file_view(request):
    if request.method == 'POST' and request.FILES.get('uploaded_file'):
        uploaded_file = request.FILES['uploaded_file']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        safe_filename = timestamp + uploaded_file.name
        original_filename = uploaded_file.name  # 元のファイル名を保存
        
        file_path = os.path.join(settings.MEDIA_ROOT, safe_filename)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return JsonResponse({
            'message': 'ファイルが正常にアップロードされました。',
            'file_name': safe_filename,
            'original_filename': original_filename,  # 元のファイル名を追加
            'file_url': settings.MEDIA_URL + safe_filename
        })

    return JsonResponse({'error': 'アップロードに失敗しました。'}, status=400)