from django.contrib import admin
from . models import PurchasementType, PurchasementStep, PurchasementItem

class PurchasementStepAdmin(admin.ModelAdmin):
    list_display = ('id','name','number','project_type','purchasement_type' )
    search_fields = ['name']
    list_filter = ['project_type']
    

class PurchasementTypeAdmin(admin.ModelAdmin):
    list_display = ('id','code','description','number')
   
class PurchasementItemAdmin(admin.ModelAdmin):
    list_display = ('id','name','number','project_type','purchasement_type' )
    search_fields = ['name']
    list_filter = ['project_type','purchasement_type' ]

admin.site.register(PurchasementItem,PurchasementItemAdmin)
admin.site.register(PurchasementStep,PurchasementStepAdmin)
admin.site.register(PurchasementType,PurchasementTypeAdmin)