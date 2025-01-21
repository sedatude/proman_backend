from django.contrib import admin
from . models import PurchasementType, PurchasementStep, PurchasementItem

class PurchasementStepAdmin(admin.ModelAdmin):
    list_display = ('id','name','no','project_type','purchasement_type' )
    search_fields = ['name']
    list_filter = ['project_type']
    

class PurchasementTypeAdmin(admin.ModelAdmin):
    list_display = ('id','code','description','no')
   
class PurchasementItemAdmin(admin.ModelAdmin):
    list_display = ('id','name','no','project_type','purchasement_type' )
    search_fields = ['name']
    list_filter = ['project_type','purchasement_type' ]

admin.site.register(PurchasementItem,PurchasementItemAdmin)
admin.site.register(PurchasementStep,PurchasementStepAdmin)
admin.site.register(PurchasementType,PurchasementTypeAdmin)