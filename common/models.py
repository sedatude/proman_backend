from django.db import models
import datetime

 
 
 
class Logs(models.Model):
    site = models.CharField(blank=True, max_length=50)
    text = models.CharField(blank=True, max_length=500)
    created_at = models.DateTimeField(blank=True, null=True)    
    type = models.CharField(max_length=50, blank=True)
    record_id = models.IntegerField(default=1)
    user_info = models.CharField(blank=True, max_length=50)
    is_error =models.BooleanField(default=False)  

    class Meta:
        db_table = 'logs' 
        
    def __str__(self):
        return self.text

    
    def save_log(site,text,type,record_id,user_info,is_error=False):
        """Save logs and error, if error send True otherwise it will be log record.
            site: is the function name
            text: is the message
            type: is used for grouping logs and errors
            is_error: is last variable;Set it true otherwise dont send it
            """
        
        Logs(site=site, text=text[0:500], created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), type=type
          ,record_id=record_id, user_info=user_info[0:50],is_error=is_error).save()
        #error#Logs.save_log("edit_dividend", f'Total:{str(counter)} dividend added for {company.name}', "company", id, request.user.first_name+" "+request.user.last_name,True )
        #Logs.save_log("process_acceptment_production", str_message, "production", production.id, request.user.first_name+" "+request.user.last_name)
        #Logs.save_log("special_product_entry", f'{str(product.name)}+  adlı ürün için özel malzeme listesi oluşturldu.', "special_product", production.id, request.user.first_name+" "+request.user.last_name)



 

class Money(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Para Birimi Adı")
    short = models.CharField(max_length=10, unique=True, verbose_name="Kısa Adı")
    symbol = models.CharField(max_length=10, verbose_name="Sembol")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        verbose_name = 'Money'    
        verbose_name_plural = 'Monies'
        db_table = 'money'  
    def __str__(self):
        return f'{self.symbol} {self.short}'


class MoneyRate(models.Model):
    money = models.ForeignKey(Money, related_name="rates", on_delete=models.CASCADE, verbose_name="Para Birimi")
    price = models.DecimalField(max_digits=15, decimal_places=4, verbose_name="Kur Değeri")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")
    class Meta:
        verbose_name = 'Money Rate'    
        verbose_name_plural = 'Rates'
        db_table = 'money_rate' 
    def __str__(self):
        return f"{self.money.short} - {self.price} ({self.date.strftime('%Y-%m-%d')})"

