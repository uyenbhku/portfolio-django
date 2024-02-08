from django.contrib import admin

# Import your models here.
from .models import Project, ContactInfo, MySkill, MyLanguage, MyTool, MyTitle, MyInfo


# Register your models here.
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

admin.site.register(ContactInfo, ContactInfoAdmin)



class ProjectAdmin(admin.ModelAdmin):
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

admin.site.register(Project, ProjectAdmin)



class MySkillInline(admin.TabularInline):
    model = MySkill


class MyLanguageInline(admin.TabularInline):
    model = MyLanguage


class MyTitleInline(admin.TabularInline):
    model = MyTitle


class MyToolInline(admin.TabularInline):
    model = MyTool



class MyInfoAdmin(admin.ModelAdmin):
    model = MyInfo
    inlines = [
        MyTitleInline,
        MyLanguageInline,
        MySkillInline,
        MyToolInline,
    ]
admin.site.register(MyInfo, MyInfoAdmin)


# admin.site.unregister([
#     MySkill,
#     MyLanguage,
#     MyInfo,
#     MyTool,
#     MyTitle,
#     ])
# admin.site.register([
#     MySkill,
#     MyLanguage,
#     MyInfo,
#     MyTool,
#     MyTitle,], MyInfoAdmin)
