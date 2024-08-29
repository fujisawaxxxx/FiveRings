from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  # ログインが必要なビューとして設定
def main_view(request):
    return render(request, 'accounts/main.html')
