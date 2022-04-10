from django.conf import settings
from django.contrib import admin

from .models import Group, Post

EMPTY_VALUE = settings.DEFAULT_LABEL_VALUE


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = EMPTY_VALUE


admin.site.register(Group)
