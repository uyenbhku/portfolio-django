# from django.contrib import admin

# # Import your models here.
# from .models import Project, ContactInfo, MySkill, MyLanguage, MyTool, MyTitle, MyInfo


# # Register your models here.
# class ContactInfoAdmin(admin.ModelAdmin):
#     list_display = [
#         'name',
#         'email', 
#         'message',
#     ]

#     search_fields = [
#         'name',
#         'email',
#     ]

# admin.site.register(ContactInfo, ContactInfoAdmin)



# class ProjectAdmin(admin.ModelAdmin):
#     list_display = [
#         'title', 
#         'course_name',
#         'date',
#         'is_hidden',
#         'live_url',
#     ]

#     list_filter = [
#         'tag',
#         'course_name',
#         'date',
#         'is_hidden',
#     ]

#     search_fields = [
#         'title',
#         'course_name',
#     ]

# admin.site.register(Project, ProjectAdmin)



# class MySkillInline(admin.TabularInline):
#     model = MySkill


# class MyLanguageInline(admin.TabularInline):
#     model = MyLanguage


# class MyTitleInline(admin.TabularInline):
#     model = MyTitle


# class MyToolInline(admin.TabularInline):
#     model = MyTool



# class MyInfoAdmin(admin.ModelAdmin):
#     model = MyInfo
#     inlines = [
#         MyTitleInline,
#         MyLanguageInline,
#         MySkillInline,
#         MyToolInline,
#     ]
# admin.site.register(MyInfo, MyInfoAdmin)


# # admin.site.unregister([
# #     MySkill,
# #     MyLanguage,
# #     MyInfo,
# #     MyTool,
# #     MyTitle,
# #     ])
# # admin.site.register([
# #     MySkill,
# #     MyLanguage,
# #     MyInfo,
# #     MyTool,
# #     MyTitle,], MyInfoAdmin)
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Project, Technology, Education, WorkExperience,
    Profile, BlogPost, ContactMessage
)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'profile',
        'status',
        'display_technologies',
        'created_at',
        'is_featured',
        'is_hidden',
        'priority',
        'preview_link'
    ]
    
    list_filter = [
        'status',
        'is_featured',
        'is_hidden',
        'technologies',
        'created_at'
    ]
    
    search_fields = [
        'title',
        'description',
        'short_description'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    
    filter_horizontal = ['technologies']
    
    def display_technologies(self, obj):
        return ", ".join([tech.name for tech in obj.technologies.all()])
    display_technologies.short_description = 'Technologies'
    
    def preview_link(self, obj):
        if obj.live_url:
            return format_html('<a href="{}" target="_blank">View Live</a>', obj.live_url)
        return "No preview"
    preview_link.short_description = 'Preview'

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'level',
        'is_featured',
        'is_hidden',
        'project_count'
    ]
    
    list_filter = ['category', 'is_featured', 'is_hidden']
    search_fields = ['name']
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Used in Projects'

class ExperienceAdminMixin:
    list_display = [
        'title',
        'organization',
        'location',
        'start_date',
        'end_date',
        'is_current'
    ]
    
    list_filter = ['is_current', 'organization']
    search_fields = ['title', 'organization', 'description']
    ordering = ['-start_date']

@admin.register(Education)
class EducationAdmin(ExperienceAdminMixin, admin.ModelAdmin):
    list_display = ExperienceAdminMixin.list_display + ['degree', 'field_of_study']

@admin.register(WorkExperience)
class WorkExperienceAdmin(ExperienceAdminMixin, admin.ModelAdmin):
    filter_horizontal = ['technologies_used']
    
    def get_list_display(self, request):
        return ExperienceAdminMixin.list_display + ['display_technologies']
    
    def display_technologies(self, obj):
        return ", ".join([tech.name for tech in obj.technologies_used.all()])
    display_technologies.short_description = 'Technologies Used'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'location']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'title', 'email', 'phone', 'location')
        }),
        ('Biography', {
            'fields': ('bio_short', 'bio_full')
        }),
        ('Social Media', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url')
        }),
        ('Files', {
            'fields': ('resume', 'profile_image')
        })
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'status',
        'profile',
        'created_at',
        'published_at',
        'preview_link'
    ]
    
    list_filter = ['status', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    
    filter_horizontal = ['technologies']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('profile', 'title', 'slug', 'content', 'excerpt')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at')
        }),
        ('Media', {
            'fields': ('featured_image', 'technologies')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def preview_link(self, obj):
        if obj.status == 'published':
            return format_html('<a href="{}" target="_blank">View Post</a>', 
                             obj.get_absolute_url())
        return "Draft"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'subject',
        'created_at',
        'is_read'
    ]
    
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"