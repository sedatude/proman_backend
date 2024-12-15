from django.contrib import admin

from company.models import Company, CompanyType
from common.models import Money, MoneyRate 
 

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','name', )
    #list_filter = ['usage_type', 'type']
    search_fields = ['name',]

class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name'   )
 
 

class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id','name','short','symbol')

class MoneyRateAdmin(admin.ModelAdmin):
    list_display = ('id','money_id','price','date')
 
 
admin.site.register(Money,MoneyAdmin)

admin.site.register(MoneyRate,MoneyRateAdmin)

admin.site.register(CompanyType,CompanyTypeAdmin)
admin.site.register(Company,CompanyAdmin)
 