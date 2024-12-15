from django.db import models
from common.models import Money
from project.models import Project, ProjectType
from account.models import Account




class PurchasementType(models.Model):
    code = models.CharField(max_length=10, default='', verbose_name="Code (EN)")
    description = models.CharField(max_length=255, default='', verbose_name="Description (EN)")
    code_tr = models.CharField(max_length=10, default='', verbose_name="Code")
    description_tr = models.CharField(max_length=255, default='', verbose_name="Description")
    number = models.PositiveSmallIntegerField(default=1)
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
    number = models.PositiveSmallIntegerField(default=1, verbose_name="Item Number")
    
    purchasement_type = models.ForeignKey(
        PurchasementType, 
        related_name='purchasement_items', 
        on_delete=models.DO_NOTHING, 
        default=1,
        verbose_name="Purchasement Type"
    )
    project_type = models.ForeignKey(
        ProjectType, 
        related_name='project_items', 
        on_delete=models.DO_NOTHING, 
        default=1,
        verbose_name="Project Type"
    )
 
    class Meta:
        db_table = 'purchasement_item'
        verbose_name = "Purchasement Item"
        verbose_name_plural = "Purchasement Items"
        ordering = ['number']  # Sıralama için

    def __str__(self):
        return f"{self.name} - {self.purchasement_type}"
  


class PurchasementStep(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Step Name")
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
    number = models.PositiveSmallIntegerField(default=1)
    # 2	SOLAR CABLE	2	Solar Power Plant	GB: GOODS BIG
	# 1	PV MODULE & CONNECTOR	1	Solar Power Plant	GB: GOODS BIG
    
    class Meta:
        db_table = 'purchasement_step'   

class CostItem(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='project_cost_items', 
        on_delete=models.DO_NOTHING, 
        default=1, 
        verbose_name="Project"
    )
    purchasement_step = models.ForeignKey(
        PurchasementStep, 
        related_name='step_cost_items', 
        on_delete=models.DO_NOTHING, 
        default=1, 
        verbose_name="Purchasement Step"
    )

    name = models.CharField(max_length=255, unique=True, verbose_name="Cost Item Name")
    number = models.SmallIntegerField(default=1, verbose_name="Number")
    description = models.TextField(verbose_name="Description", blank=True)

    # Yeni eklenen alanlar
    made_in = models.CharField(max_length=50, verbose_name="Made In", blank=True)
    supplier = models.CharField(max_length=255, verbose_name="Supplier", blank=True)
    producer_brand = models.CharField(max_length=255, verbose_name="Producer (Brand)", blank=True)
    customs_required = models.BooleanField(default=False, verbose_name="Customs Required")
    pa = models.BooleanField(default=False, verbose_name="PA")
    pm = models.BooleanField(default=False, verbose_name="PM")
    pd = models.BooleanField(default=False, verbose_name="PD")
    notes = models.TextField(verbose_name="Notes", blank=True)

    # Mevcut alanlar
    material = models.CharField(max_length=255, verbose_name="Material")
    brand = models.CharField(max_length=255, verbose_name="Brand", blank=True)
    quantity = models.IntegerField(default=1, verbose_name="Quantity")
    unit = models.CharField(max_length=50, verbose_name="Unit")
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Unit Price"
    )
    total_price = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Total Price"
    )
    currency = models.ForeignKey(
        Money, 
        related_name='cost_items', 
        on_delete=models.PROTECT, 
        verbose_name="Currency"
    )
    detail_description = models.TextField(verbose_name="Detail Description", blank=True)

    class Meta:
        db_table = 'cost_item'

    def __str__(self):
        return f"{self.name} - {self.material}"


 
class TaskDetail(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='task_details', 
        on_delete=models.DO_NOTHING, 
        default=1, 
        verbose_name="Project"
    )
    step = models.ForeignKey(
        PurchasementStep, 
        related_name='task_steps', 
        on_delete=models.DO_NOTHING,
        verbose_name="Step"
    )
    assigned = models.ForeignKey(
        Account,
        related_name='assigned_tasks', 
        on_delete=models.DO_NOTHING, 
        verbose_name="Assigned User"
    )
    owner = models.ForeignKey(
        Account,
        related_name='owned_tasks', 
        on_delete=models.DO_NOTHING, 
        verbose_name="Owner User"
    )
    duration = models.CharField(max_length=50, verbose_name="Duration", blank=True, null=True)
    start = models.DateField(verbose_name="Start Date", blank=True, null=True)
    finish = models.DateField(verbose_name="Finish Date", blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name="Title")
    progress = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Progress (%)", 
        default=0.00
    )
    progress_comments = models.TextField(verbose_name="Progress Comments", blank=True, null=True)
    status = models.CharField(max_length=50, verbose_name="Status", blank=True, null=True)
    complete_date = models.DateField(verbose_name="Complete Date", blank=True, null=True)
    md_approval_status = models.CharField(max_length=50, verbose_name="MD Approval Status", blank=True, null=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)
    
    class Meta:
        db_table = 'task_detail'
        verbose_name = "Task Detail"
        verbose_name_plural = "Task Details"

    def __str__(self):
        return self.title
