from django.contrib import admin
from .models import Card, CardDriverHistory

class CardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'driver', 'company')
    search_fields = ('card_number',)


admin.site.register(Card, CardAdmin)
admin.site.register(CardDriverHistory)