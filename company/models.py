 
from django.db import models
import uuid
from PIL import  Image



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    
    file_path = str(instance.id)+'/'+filename
    uniq = uuid.uuid1()
    file_path = str(instance.id)+'/'+str(uniq)+filename
    return file_path

class CompanyType(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    """"
    1	Müşteri
	2	Tedarikçi
	3	Program Sahibi
    """
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = 'Company Type'    
        verbose_name_plural = 'Company Types'
        db_table = 'company_types'  
 

class Company(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(default='logo.png', upload_to= user_directory_path)
    address = models.TextField(max_length=500, blank=True)
    registration_no = models.CharField(max_length=500, blank=True) #account  number or iban
    tax_number = models.CharField(max_length=50, blank=True, null=True )
    tax_place = models.CharField(max_length=100, blank=True, null=True )
    web_site = models.CharField(max_length=100, blank=True, null=True )
    email = models.CharField(max_length=100,  blank=True, null=True )
    phone = models.CharField(max_length=100,  blank=True, null=True )
    second_phone = models.CharField(max_length=100,  blank=True, null=True )
    contact_name = models.CharField(max_length=100,  blank=True, null=True )
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=500, blank=True, null=True )
    type = models.ForeignKey(CompanyType, on_delete=models.DO_NOTHING, default=2)
    class Meta:
        verbose_name = 'company'    
        verbose_name_plural = 'companies'
        db_table = 'company'                


    def __str__(self):
        return f'{self.name}'

    def save(self, *agrs, **kwargs):
        super().save(*agrs, **kwargs)
        if self.logo:
            img = Image.open(self.logo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.logo.path)

    









    

     