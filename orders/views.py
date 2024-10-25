from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import CaseCard

def get_case_card_price(request):
    content = request.GET.get('content', None)

    # contentが指定されている場合、そのnumber_of_sheetsに一致するケースカードを取得
    if content is not None:
        try:
            case_card = CaseCard.objects.get(number_of_sheets=content)
            return JsonResponse({'unit_price': case_card.unit_price})
        except CaseCard.DoesNotExist:
            return JsonResponse({'error': 'No matching case card found'}, status=404)
    else:
        return JsonResponse({'error': 'Content parameter missing'}, status=400)
