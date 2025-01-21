from django.db import models
from common.models import Money
from project.models import Project, ProjectType
from account.models import Account




class PurchasementType(models.Model):
    code = models.CharField(max_length=10, default='', verbose_name="Code (EN)")
    description = models.CharField(max_length=255, default='', verbose_name="Description (EN)")
    code_tr = models.CharField(max_length=10, default='', verbose_name="Code")
    description_tr = models.CharField(max_length=255, default='', verbose_name="Description")
    no = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    # """	3	CS	CONSTRUCTION SMALL	3
    #     2	GB	GOODS BIG	2
    #     1	GS	GOODS SMALL	1"""
    class Meta:
        db_table = 'purchasement_type'  

    def __str__(self):
        return f"{self.code}: {self.description}"


class PurchasementItem(models.Model):
    name = models.CharField(max_length=800, verbose_name="Item Name")
    name_tr = models.CharField(max_length=800, verbose_name="Item Name (TR)")
    no = models.PositiveSmallIntegerField(default=1, verbose_name="Item Number")
    
    purchasement_type = models.ForeignKey(
        PurchasementType, 
        related_name='purchasement_items', 
        on_delete=models.DO_NOTHING, 
        default=1,
        verbose_name="Purchasement Type"
    )
    project_type = models.ForeignKey(
        ProjectType, 
        related_name='items',  # Düzenlendi
        on_delete=models.DO_NOTHING, 
        default=1,
        verbose_name="Project Type"
    )
 
    class Meta:
        db_table = 'purchasement_item'
        verbose_name = "Purchasement Item"
        verbose_name_plural = "Purchasement Items"
        ordering = ['no']  # Sıralama için

    def __str__(self):
        return f"{self.name} - {self.purchasement_type}"
  


class PurchasementStep(models.Model):
#     1	PV MODULE & CONNECTOR
# 2	SOLAR CABLE
# 3	INVERTER
# 4	CONSTRUCTION MATERIAL (TRACKER)
# 5	CIVIL&ELECTRICAL WORKS
    name = models.CharField(max_length=255, verbose_name="Step Name")
    purchasement_type = models.ForeignKey(
        PurchasementType, 
        related_name='purchasement_step_types', 
        on_delete=models.DO_NOTHING, 
        default=1,
        verbose_name="Purchasement Type"
    )
    project_type = models.ForeignKey(
        ProjectType, 
        related_name='purchasement_steps', 
        on_delete=models.DO_NOTHING, 
        default=1,
        verbose_name="Project Type"
    )
    no = models.PositiveSmallIntegerField(default=1)
    # 2	SOLAR CABLE	2	Solar Power Plant	GB: GOODS BIG
	# 1	PV MODULE & CONNECTOR	1	Solar Power Plant	GB: GOODS BIG
    
    class Meta:
        db_table = 'purchasement_step'   

""""burada ilk gelen adımlar var alt adımlar değil """
class PurchasementStepDetail(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='step_details',  # Düzenlendi
        on_delete=models.DO_NOTHING, 
        default=1, 
        verbose_name="Project"
    )
    purchasement_step = models.ForeignKey(
        PurchasementStep, 
        related_name='details',  # Düzenlendi
        on_delete=models.DO_NOTHING, 
        default=1, 
        verbose_name="Purchasement Step"
    )

    purchasement_type = models.CharField(
        max_length=255, 
        verbose_name="Cost Item Name", 
        null=True
    )
    name = models.CharField(
        max_length=255, 
        verbose_name="Cost Item Name", 
        null=True
    )
    no = models.SmallIntegerField(
        default=1, 
        verbose_name="Number", 
        null=True
    )
    description = models.TextField(
        verbose_name="Description", 
        blank=True, 
        null=True
    )

    made_in = models.CharField(
        max_length=250, 
        verbose_name="Made In", 
        blank=True, 
        null=True
    )
    supplier = models.CharField(
        max_length=255, 
        verbose_name="Supplier", 
        blank=True, 
        null=True
    )
    producer_brand = models.CharField(
        max_length=500, 
        verbose_name="Producer (Brand)", 
        blank=True, 
        null=True
    )
 
    customs_required = models.CharField(
        max_length=3, 
       default= '?',
       )
    pa = models.ForeignKey(
        Account, 
        on_delete=models.SET_NULL, 
        verbose_name="PA", 
        null=True, 
        blank=True,
        related_name='pa_items'  # Düzenlendi
    )
    pm = models.ForeignKey(
        Account, 
        on_delete=models.SET_NULL, 
        verbose_name="PM", 
        null=True, 
        blank=True,
        related_name='pm_items'  # Düzenlendi
    )
    pd = models.ForeignKey(
        Account, 
        on_delete=models.SET_NULL, 
        verbose_name="PD", 
        null=True, 
        blank=True,
        related_name='pd_items'  # Düzenlendi
    )

    notes = models.TextField(
        verbose_name="Notes", 
        blank=True, 
        null=True
    )


    currency = models.ForeignKey(
        Money, 
        related_name='cost_items', 
        on_delete=models.PROTECT, 
        verbose_name="Currency", 
        default=1
    )

 
    class Meta:
        db_table = 'purchasement_step_detail'

    def __str__(self):
        return f"{self.name}"


 #burada  alt adımlar var 
class PurchasementDetail(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='purchasement_details', 
        on_delete=models.DO_NOTHING, 
        default=1, 
        verbose_name="Project"
    )

    purchasement_type = models.ForeignKey(
        PurchasementType, 
        related_name='purchasement_types', # 3	INVERTER
        on_delete=models.DO_NOTHING,
        verbose_name="Step"
    )
    purchasement_step_detail = models.ForeignKey(
        PurchasementStepDetail, 
        related_name='purchasement_details', 
        on_delete=models.DO_NOTHING,
        verbose_name="Purchasement Step Detail"
    )
    purchasement_item = models.ForeignKey(
        PurchasementItem, 
        related_name='purchasement_items', 
        on_delete=models.DO_NOTHING,
        verbose_name="purchasement item"
    )

    name = models.CharField(max_length=1200, verbose_name="Step Name")
    title = models.CharField(max_length=1200, verbose_name="Title Name")

    assigned_users = models.ManyToManyField(
        Account,
        related_name='assigned_tasks', 
        verbose_name="Assigned Users"
    )
    owner = models.ForeignKey(
        Account,
        related_name='owned_purchasements', 
        on_delete=models.DO_NOTHING, 
        verbose_name="Owner User"
    )
    duration = models.CharField(max_length=50, verbose_name="Duration", blank=True, null=True)
    start_date = models.DateField(verbose_name="Start Date", blank=True, null=True)
    finish_date = models.DateField(verbose_name="Finish Date", blank=True, null=True)
    progress = models.PositiveSmallIntegerField(
        verbose_name="Progress (%)", 
        default=0
    )
    progress_comments = models.TextField(verbose_name="Progress Comments", blank=True, null=True)
    status = models.CharField(max_length=50, verbose_name="Status", default="")
    complete_date = models.DateField(verbose_name="Complete Date", blank=True, null=True)
    md_approval_status = models.CharField(max_length=50, verbose_name="MD Approval Status", default="")
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)
    no = models.PositiveSmallIntegerField(default=1)
    
    class Meta:
        db_table = 'purchasement_detail'
        verbose_name = "Purchasement Detail"
        verbose_name_plural = "Purchasement Details"

    def __str__(self):
        return self.title
