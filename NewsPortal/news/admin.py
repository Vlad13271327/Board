from django.contrib import admin
from .models import Post, Category, PostCategory

class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1

class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CategoryInline,)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)