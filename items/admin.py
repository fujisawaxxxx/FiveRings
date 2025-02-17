from django.contrib import admin
from .models import AgreementColor
from .models import AgreementMonochrome
from .models import CaseCard
from .models import Chiken
from .models import Fukuyaku
from .models import ParticipationCard

admin.site.register(AgreementColor)
admin.site.register(AgreementMonochrome)
admin.site.register(CaseCard)
admin.site.register(Chiken)
admin.site.register(Fukuyaku)
admin.site.register(ParticipationCard)