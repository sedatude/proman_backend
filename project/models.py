from django.db import models
from account.models import Account
from company.models import Company
from common.models import Money
from django.utils.timezone import now

class ProjectType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Project Name")
    description = models.TextField(verbose_name="Description", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        db_table = 'project_type'  
 

    def __str__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Proje Adı")
    owner = models.ForeignKey(Company, related_name='project_owner', on_delete=models.DO_NOTHING, default=1)
    company = models.ForeignKey(Company, related_name='project_company', on_delete=models.DO_NOTHING, default=1)
    project_type = models.ForeignKey(ProjectType, related_name='project_type', on_delete=models.DO_NOTHING, default=1)
    description = models.TextField(verbose_name="Açıklama", blank=True)
    start_date = models.DateField(verbose_name="Başlangıç Tarihi", default=now)
    estimated_end_date = models.DateField(verbose_name="Tahmini Bitiş Tarihi", default=now)
    updated_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi")
    completed_at = models.DateField(null=True, blank=True, verbose_name="Bitiş Tarihi")
    creater = models.ForeignKey(
        Account, 
        on_delete=models.SET_NULL, 
        verbose_name="Project Creater", 
        null=True, 
        blank=True,
        related_name='creater_project'
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active") 
    is_template = models.BooleanField(default=True, verbose_name="Is Template") 

    class Meta:
        db_table = 'project'  

    def __str__(self):
        return self.name
    


 
