from django.contrib import admin

# Import your models here.
from .models import Article, ContactInfo
# Register your models here.
admin.site.register([
    Article, 
    ContactInfo
])


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email', 
        'message',
    ]

    search_fields = [
        'name',
        'email',
    ]

admin.site.unregister(ContactInfo)
admin.site.register(ContactInfo, ContactInfoAdmin)



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