from django.contrib import admin
from .models import AgreementColor
from .models import AgreementMonochrome
from .models import CaseCard

admin.site.register(AgreementColor)
admin.site.register(AgreementMonochrome)
admin.site.register(CaseCard)