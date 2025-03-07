from django.contrib import admin
from .models import Post, Category, PostCategory

class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1

class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CategoryInline,)
    list_display = ('title', 'get_categories', 'date_in')
    list_filter = ('title', 'category', 'rating')
    search_fields = ('title', 'category__name')

    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])
    get_categories.short_description = 'Категории'


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)