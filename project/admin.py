
from django.contrib import admin
from project.models import Project, ProjectType

 
# class Project_StockInline(NestedTabularInline):
#     model = Project_Stock
#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_add_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name','owner','company' )
    search_fields = ['name']
    

admin.site.register(Project,ProjectAdmin)
admin.site.register(ProjectType)
 