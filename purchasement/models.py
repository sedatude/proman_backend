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
#     1	PV MODULE & CONNECTOR
# 2	SOLAR CABLE
# 3	INVERTER
# 4	CONSTRUCTION MATERIAL (TRACKER)
# 5	CIVIL&ELECTRICAL WORKS
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
    number = models.SmallIntegerField(
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
  # ...existing code...
    customs_required = models.BooleanField(
        default=False, 
        verbose_name="Customs Required"
    )
    pa = models.ForeignKey(
        'Account', 
        on_delete=models.SET_NULL, 
        verbose_name="PA", 
        null=True, 
        blank=True
    )
    pm = models.ForeignKey(
        'Account', 
        on_delete=models.SET_NULL, 
        verbose_name="PM", 
        null=True, 
        blank=True
    )
    pd = models.ForeignKey(
        'Account', 
        on_delete=models.SET_NULL, 
        verbose_name="PD", 
        null=True, 
        blank=True
    )
# ...existing code...
    notes = models.TextField(
        verbose_name="Notes", 
        blank=True, 
        null=True
    )
# ...existing code...
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
