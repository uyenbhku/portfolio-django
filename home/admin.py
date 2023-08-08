from django.contrib import admin

# Register your models here.
from .models import Article
# Register your models here.
admin.site.register(Article)

class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'course_name',
        'date',
    ]

    list_filter = [
        'tag',
        'course_name',
        'date',
    ]

    search_fields = [
        'title',
        'course_name',
    ]

admin.site.unregister(Article)
admin.site.register(Article, ArticleAdmin)