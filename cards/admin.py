from django.contrib import admin
from cards.forms import TagForm

from cards.models import Card, Item, Tag

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    form = TagForm


admin.site.register(Card)
admin.site.register(Item)
admin.site.register(Tag, TagAdmin)