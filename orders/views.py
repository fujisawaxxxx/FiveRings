from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import CaseCard,Chiken,Fukuyaku

# ケースカード
def get_case_card_price(request):
    content = request.GET.get('content', None)

    # contentが指定されている場合、そのnumber_of_sheetsに一致するケースカードを取得
    if content is not None:
        try:
            case_card = CaseCard.objects.get(number_of_sheets=content)
            return JsonResponse({'unit_price': case_card.unit_price})
        except CaseCard.DoesNotExist:
            return JsonResponse({'error': 'ケースカードが見つかりません'}, status=404)
    else:
        return JsonResponse({'error': 'ケースカードのパラメーターが見つかりました'}, status=400)


# 治験実施計画書
def get_chiken_plan_price(request):
    content = request.GET.get('content', None)

    # contentが指定されている場合、そのnumber_of_sheetsに一致するケースカードを取得
    if content is not None:
        try:
            chiken_plan = Chiken.objects.get(number_of_sheets=content)
            return JsonResponse({'unit_price': chiken_plan.unit_price})
        except Chiken.DoesNotExist:
            return JsonResponse({'error': '治験実施計画書が見つかりません'}, status=404)
    else:
        return JsonResponse({'error': '治験実施計画書のパラメーターが見つかりました'}, status=400)

# 服薬日誌
def get_medication_diary_price(request):
    content = request.GET.get('content', None)

    # contentが指定されている場合、そのnumber_of_sheetsに一致するケースカードを取得
    if content is not None:
        try:
            medication_diary = Fukuyaku.objects.get(number_of_sheets=content)
            return JsonResponse({'unit_price': medication_diary.unit_price})
        except Fukuyaku.DoesNotExist:
            return JsonResponse({'error': '服薬日誌が見つかりません'}, status=404)
    else:
        return JsonResponse({'error': '服薬日誌のパラメーターが見つかりました'}, status=400)