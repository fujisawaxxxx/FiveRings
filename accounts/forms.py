from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="必須です。有効なメールアドレスを入力してください。")
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "必須です。150文字以下の英数字と記号(@/./+/-/_)のみ使用できます。"
        self.fields['password1'].help_text = "8文字以上で、数字と文字を含める必要があります。"
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # 自動的にスタッフ権限を付与
        user.is_staff = True
        
        if commit:
            user.save()
            
            # 閲覧のみグループを取得または作成して自動的に追加
            view_only_group, created = Group.objects.get_or_create(name="閲覧のみグループ")
            user.groups.add(view_only_group)
                
        return user
