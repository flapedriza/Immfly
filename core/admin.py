from django.contrib import admin

# Register your models here.
from core.models import Channel, Rating, Content


class ContentAdmin(admin.ModelAdmin):
    exclude = ('rating',)


admin.site.register(Channel)
admin.site.register(Rating)
admin.site.register(Content, ContentAdmin)
