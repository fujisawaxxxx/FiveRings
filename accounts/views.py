# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
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

    context = {
        'product_type': product_type,
        'quantity': quantity,
        'content': content,
        'unit_price': unit_price,
        'estimate_result': estimate_result,
    }

    return render(request, 'accounts/create_order.html', context)


@login_required
def upload_file_view(request):
    if request.method == 'POST' and request.FILES.get('uploaded_file'):
        uploaded_file = request.FILES['uploaded_file']
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return JsonResponse({'message': 'ファイルが正常にアップロードされました。', 'file_name': uploaded_file.name})

    return JsonResponse({'error': 'アップロードに失敗しました。'}, status=400)