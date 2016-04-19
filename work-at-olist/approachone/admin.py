from django.contrib import admin
from .models import Category
from .models import Channel


class ChannelAdmin(admin.ModelAdmin):
    filter_horizontal = ['category_set']

admin.site.register(Channel, ChannelAdmin)
admin.site.register(Category)

