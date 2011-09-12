from django.contrib import admin
from core.models import *
from attachments.admin import AttachmentInlines
from object_permissions.admin import ObjectPermissionInline

class TicketAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]

class NewsAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]

class VersionInline(admin.TabularInline):
    model = Version
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines, ObjectPermissionInline, VersionInline]

admin.site.register(Project,ProjectAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(Status)
admin.site.register(Version)
admin.site.register(Priority)
admin.site.register(Role)
admin.site.register(News,NewsAdmin)
admin.site.register(Category)
