from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title',  'text', 'author', 'date_in']
    list_filter = ('author', 'date_in')

admin.site.register(Post, PostAdmin)
