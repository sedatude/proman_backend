from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from numpy import product
 
from common.models import Money
from company.models import Company
from purchasement.models import PurchasementStepDetail, PurchasementItem

from account.models import Account, UserAuth, UserProfile
import os, pandas as pd
from django.contrib import messages, auth
from django.db.models.functions import Cast, Coalesce, TruncDate
from django.db.models import Count, TextField, F, Sum,Max,Q
from django.db.models import FloatField, TextField

from purchasement.models import PurchasementStep, PurchasementType
from project.models import Project, ProjectType
 # Model adını doğru kullan
from django.db import transaction

def import_purchasement_items(request):
    # Tüm eski kayıtları sil
    purchasement_type=2
    data = []
    for i in range(1,7):
        purchasement_type = i
        if purchasement_type == 1: #1	GS
            data = [
    {"no": 1, "name": "Please define the procurement, enter the relevant date and assign a PM for this procurement. You must also give GS warning."},
    {"no": 2, "name": "Please prepare and update proposal request form. Request and gather proposals from suppliers. Archive proposals and proformas digitally."},
    {"no": 3, "name": "Please check the digital archive. Submit the proposal comparison chart to PD for approval with PM's supervision."},
    {"no": 4, "name": "Please prepare a Project Purchasement (PO)."},
    {"no": 5, "name": "Please review the contents of the PO and assign PO number. Then, have the supplier sign the contract and submit it to PD for approval."},
    {"no": 6, "name": "Please review the PO. Pay in advance. If necessary, add to the checklist. In addition, please inform the accounting department about the advance payment with the PO number. Upload the advance payment receipt to this row."},
    {"no": 7, "name": "Please add the purchasement to the PO list."},
    {"no": 8, "name": "Please organize the delivery after product is ready. If necessary, request the second payment from PD."},
    {"no": 9, "name": "Please check the contract and make the second payment due if needed. Please also notify the accounting department about this second advance payment with the Project Purchasement Number (PO No)."},
    {"no": 10, "name": "Before unloading, please ensure that the goods have been received in the correct quantity and are free of any defects. If everything is in order, please prepare delivery notes and photographs and upload the documents here according to the attached sample. In the event of goods being damaged or missing, please contact the supplier by email and phone, and contact PM and PD to request a solution. If PD or PM decide to unload these issued goods, please take detailed videos and photos before and after unloading. If you encounter this issue during or after unloading, please halt the work and follow the steps outlined above."},
    {"no": 11, "name": "Please check all documents received from SM. Please also archive all documents as hard (wet ink) and soft copies."},
    {"no": 12, "name": "Please ensure that all documents above have been archived as hard (wet ink) and soft copies."},
    {"no": 13, "name": "Please ensure that the invoice is issued correctly by supplier according to the attached sample. Additionally, please review the contract and invoice together."},
    {"no": 14, "name": "Please check the PO and make the remaining payment if necessary. Additionally, please inform the accounting department about the payment with the PO number."},
    {"no": 15, "name": "Please check the invoice of the exchange rate difference according to the payments made. If necessary, obtain approval from the PD to close the process accounting-wise by offsetting the payment or exchange difference invoices."},
    {"no": 16, "name": "Please make final checks of the entire process and obtain confirmation from the PD that the work has been completed."}
]


        elif purchasement_type == 2: #	GB
            data = [
    {"no": 1, "name": "Please define the procurement, enter the relevant date and assign a PM for this procurement. You must also give GS warning."},
    {"no": 2, "name": "Please use the attached pre-prepared administrative specification as a template and update it accordingly. In addition, please prepare a technical specification for this purchase and attach it to your updated administrative specification."},
    {"no": 3, "name": "Please prepare and update proposal request form. Request and gather proposals from suppliers. Archive proposals and proformas digitally."},
    {"no": 4, "name": "Please prepare and update the proposal comparison chart. Submit the chart to PM."},
    {"no": 5, "name": "Please check the digital archive. Submit the proposal comparison chart to PD for approval."},
    {"no": 6, "name": "Please use the attached pre-prepared contract as a template and update the yellow highlighted sections accordingly. In addition, please attach the contract as ready for signing. If necessary, please consult an attorney regarding the contract."},
    {"no": 7, "name": "Please review the contents of the contract and assign Project Purchasement (PO) number. Have the supplier sign the contract and submit it to PD for approval."},
    {"no": 8, "name": "Please review and sign the contract."},
    {"no": 9, "name": "Please review the contract. Pay in advance. If necessary, add to the checklist. In addition, please inform the accounting department about the advance payment with the PO number. Upload the advance payment receipt to this row."},
    {"no": 10, "name": "Please add the purchasement to the PO list."},
    {"no": 11, "name": "Please organize the delivery after product is ready. If necessary, request the second payment from MD."},
    {"no": 12, "name": "Please check the contract and make the second payment due if needed. Please also notify the accounting department about this second advance payment with the Project Purchasement Number (PO No)."},
    {"no": 13, "name": "Please evaluate the necessity of the FAT and also please evaluate whether the customer needed in the FAT."},
    {"no": 14, "name": "Please ensure that all test documents, material identification and certificates are obtained and archived from the manufacturer, whether FAT has been done or not."},
    {"no": 15, "name": "Check the attached instruction of insurances. According to the delivery type, please ensure the relevant insurance procedures is completed before transportation. Don't forget to unload and upload coverage. If any documentation is missing, please complete it and inform PM in the communications."},
    {"no": 16, "name": "Please check the insurance claim and the master insurance list, and add it to the current All-Risk-Insurance Policy if it is not added before. If you cannot add it to the All-Risk-Insurance policy, you can request two proposals for a new policy and submit them for approval of PD. In any case you need to finalize this procedure in this period."},
    {"no": 17, "name": "Before unloading, please ensure that the goods have been received in the correct quantity and are free of any defects. If everything is in order, please prepare delivery notes and photographs and upload the documents here according to the attached sample. In the event of goods being damaged or missing, please contact the supplier by email and phone, and contact PM and PD to request a solution. If PD or PM decide to unload these issued goods, please take detailed videos and photos before and after unloading. If you encounter this issue during or after unloading, please halt the work and follow the steps outlined above."},
    {"no": 18, "name": "Please check all documents received from SM. Please also archive all documents as hard (wet ink) and soft copies."},
    {"no": 19, "name": "Please prepare the SAT (Site Acceptance Test) or Goods Delivery Record Form and sign it according to the attached sample."},
    {"no": 20, "name": "Please check all documents received from SM. Please also archive all documents as hard (wet ink) and soft copies."},
    {"no": 21, "name": "Please ensure that all documents above have been archived as hard (wet ink) and soft copies."},
    {"no": 22, "name": "Please ensure that the invoice is issued correctly by supplier according to the attached sample. Additionally, please review the PO and invoice together."},
    {"no": 23, "name": "Please check the PO and make the remaining payment if necessary. Additionally, please inform the accounting department about the payment with the PO number."},
    {"no": 24, "name": "Please check the invoice of the exchange rate difference according to the payments made. If necessary, obtain approval from the PD to close the process accounting-wise by offsetting the payment or exchange difference invoices."},
    {"no": 25, "name": "Please make final checks of the entire process and obtain confirmation from the PD that the work has been completed."}
]


        elif purchasement_type == 3: #CS bu eksik güncellenecek
            data = [
    {"no": 1, "name": "Please define the service procurement, enter the relevant date and assign a PM for this procurement."},
    {"no": 2, "name": "Please prepare and update proposal request form. Request and gather proposals from suppliers. Archive proposals and proformas digitally."},
    {"no": 3, "name": "Please check the digital archive. Submit the proposal comparison chart to PD for approval."},
    {"no": 4, "name": "Please prepare a Project Purchasement (PO) or a contract."},
    {"no": 5, "name": "Please review the contents of the contract and assign Project Purchasement (PO) number. Have the supplier sign on the contract and Health and Safety Executive (HSE) specification, submit it to PD for approval."},
    {"no": 6, "name": "Please specify delivery of work time."},
    {"no": 7, "name": "Please review the PO. Pay in advance. If necessary, add to the checklist. In addition, please inform the accounting department about the advance payment with the PO number. Upload the advance payment receipt to this row."},
    {"no": 8, "name": "Please add the purchase and purchase schedule to PO list."},
    {"no": 9, "name": "Please evaluate the necessity of the FAT and also please evaluate whether the customer needed in the FAT."},
    {"no": 10, "name": "Please ensure that all test documents, material identification and certificates are obtained and archived from the manufacturer, whether FAT has been done or not."},
    {"no": 11, "name": "Once the product is ready, please organize the delivery. Prepare a dispatch list and photos of the delivery. If necessary, request the second payment from PD."},
    {"no": 12, "name": "Please check the HSE documents provided by the supplier for the HSE contract before starting work on site. Request on-site job training forms from the supplier. If the supplier does not have a form, please have the supplier sign on the on-site job training form. If all documents and progress are in order, please approve the starting works on site. If there are any outstanding issues, please do not allow work to begin and halt on-site operations."},
    {"no": 13, "name": "It is essential that documents be requested from PM before starting the site works. If documents are not provided by PM, please inform PD via text message. Please upload the documents in a folder as hard and soft copies."},
    {"no": 14, "name": "Please inspect the site installation works in terms of technical aspects and enforce the service supplier to apply the waste disposal rules and forms on site."},
    {"no": 15, "name": "Please require the waste disposal forms from the PM at completion of works."},
    {"no": 16, "name": "Please fill and sign Site Acceptance Test (SAT) form and have the supplier sign on the SAT."},
    {"no": 17, "name": "Please check all documents received from SM. Please also archive all documents as hard (wet ink) and soft copies."},
    {"no": 18, "name": "Please ensure that all documents above have been archived as hard (wet ink) and soft copies."},
    {"no": 19, "name": "Please ensure that the invoice is issued correctly by supplier according to the attached sample. Additionally, please review the PO and invoice together."},
    {"no": 20, "name": "Please check the PO and make the remaining payment if necessary. Additionally, please inform the accounting department about the payment with the PO number."},
    {"no": 21, "name": "Please check the invoice of the exchange rate difference according to the payments made. If necessary, obtain approval from the PD to close the process accounting-wise by offsetting the payment or exchange difference invoices."},
    {"no": 22, "name": "Please make final checks of the entire process and obtain confirmation from the PD that the work has been completed."}
]

        elif purchasement_type == 4: #CB
            data = [
    {"no": 1, "name": "Please define the service procurement, enter the relevant date and assign a PM for this procurement. You must also give CB warning."},
    {"no": 2, "name": "Please use the attached pre-prepared administrative specification as a template and update it accordingly. In addition, please prepare a technical specification for this purchase and attach it to your updated administrative specification."},
    {"no": 3, "name": "Please prepare and update proposal request form. Request and gather proposals from suppliers. Archive proposals and proformas digitally."},
    {"no": 4, "name": "Please check the digital archive. Submit the proposal comparison chart to PD for approval."},
    {"no": 5, "name": "Please use the attached pre-prepared contract as a template and update the yellow highlighted sections accordingly."},
    {"no": 6, "name": "Please review the contents of the contract and assign Project Purchasement (PO) number. Have the supplier sign on the contract and Health and Safety Executive (HSE) specification, submit it to PD for approval."},
    {"no": 7, "name": "Please specify delivery of work time."},
    {"no": 8, "name": "Please review the contract. Pay in advance. If necessary, add to the checklist. In addition, please inform the accounting department about the advance payment with the PO number. Upload the advance payment receipt to this row."},
    {"no": 9, "name": "Please add the purchase and purchase schedule to PO list."},
    {"no": 10, "name": "Please evaluate the necessity of the FAT and also please evaluate whether the customer needed in the FAT."},
    {"no": 11, "name": "Please ensure that all test documents, material identification and certificates are obtained and archived from the manufacturer, whether FAT has been done or not."},
    {"no": 12, "name": "Once the product is ready, please organize the delivery. Prepare a dispatch list and photos of the delivery. If necessary, request the second payment from PD."},
    {"no": 13, "name": "Please check the HSE documents provided by the supplier for the HSE contract before starting work on site. Request on-site job training forms from the supplier. If the supplier does not have a form, please have the supplier sign on the our on-site job training form. If all documents and progress are in order, please approve the starting works on site. If there are any outstanding issues, please do not allow work to begin and halt on-site operations."},
    {"no": 14, "name": "This is essential that documents be requested from PM before starting the site works. If documents are not provided by PM, please inform PD via text message. Please upload the documents in a folder as hard and soft copies."},
    {"no": 15, "name": "Please inspect the site installation works in terms of technical aspects and enforce the service supplier to apply the waste disposal rules and forms on site."},
    {"no": 16, "name": "Please require the waste disposal forms from the PM at completion of works."},
    {"no": 17, "name": "Please fill and sign Site Acceptance Test (SAT) form and have the supplier sign on the SAT."},
    {"no": 18, "name": "Please check all documents received from SM. Please also archive all documents as hard (wet ink) and soft copies."},
    {"no": 19, "name": "Please ensure that all documents above have been archived as hard (wet ink) and soft copies."},
    {"no": 20, "name": "Please ensure that the invoice is issued correctly by supplier according to the attached sample. Additionally, please review the PO and invoice together."},
    {"no": 21, "name": "Please check the PO and make the remaining payment if necessary. Additionally, please inform the accounting department about the payment with the PO number."},
    {"no": 22, "name": "Please check the invoice of the exchange rate difference according to the payments made. If necessary, obtain approval from the PD to close the process accounting-wise by offsetting the payment or exchange difference invoices."},
    {"no": 23, "name": "Please make final checks of the entire process and obtain confirmation from the PD that the work has been completed."}
]


        elif purchasement_type == 5: #SL
            data = [
    {"no": 1, "name": "Please define the service procurement, enter the relevant date and assign a PM for this procurement."},
    {"no": 2, "name": "Please prepare and update proposal request form. Request and gather proposals from suppliers. Archive proposals and proformas digitally."},
    {"no": 3, "name": "Please check the digital archive. Submit the proposal comparison chart to PD for approval."},
    {"no": 4, "name": "Please prepare a Project Purchasement (PO) or a contract."},
    {"no": 5, "name": "Please review the contents of the contract and assign Project Purchasement (PO) number. Have the supplier sign on the contract and Health and Safety Executive (HSE) specification, submit it to PD for approval."},
    {"no": 6, "name": "Please specify delivery of work time."},
    {"no": 7, "name": "Please review the contract. Pay in advance. If necessary, add to the checklist. In addition, please inform the accounting department about the advance payment with the PO number. Upload the advance payment receipt to this row."},
    {"no": 8, "name": "Please add the purchase and purchase schedule to PO list."},
    {"no": 9, "name": "Please check the HSE documents provided by the supplier for the HSE contract before starting work on site. Request on-site job training forms from the supplier. If the supplier does not have a form, please have the supplier sign on the our on-site job training form. If all documents and progress are in order, please approve the starting works on site. If there are any outstanding issues, please do not allow work to begin and halt on-site operations."},
    {"no": 10, "name": "This is essential that documents be requested from PM before starting the site works. If documents are not provided by PM, please inform PD via text message. Please upload the documents in a folder as hard and soft copies."},
    {"no": 11, "name": "Please inspect the site installation works in terms of technical aspects and enforce the service supplier to apply the waste disposal rules and forms on site."},
    {"no": 12, "name": "Please require the waste disposal forms from the PM at completion of works."},
    {"no": 13, "name": "Please prepare and have supplier sign work delivery record."},
    {"no": 14, "name": "Please compile the work delivery record and attachments into a single .pdf file and create hard and soft copies of the documents in a folder."},
    {"no": 15, "name": "Please ensure that all documents above have been archived as hard (wet ink) and soft copies."},
    {"no": 16, "name": "Please ensure that the invoice is issued correctly by supplier according to the attached sample. Additionally, please review the PO and invoice together."},
    {"no": 17, "name": "Please check the PO and make the remaining payment if necessary. Additionally, please inform the accounting department about the payment with the PO number."},
    {"no": 18, "name": "Please check the invoice of the exchange rate difference according to the payments made. If necessary, obtain approval from the PD to close the process accounting-wise by offsetting the payment or exchange difference invoices."},
    {"no": 19, "name": "Please make final checks of the entire process and obtain confirmation from the PD that the work has been completed."}
]


        elif purchasement_type == 6: #1	SC
            data = [
    {"no": 1, "name": "Please define the service procurement, enter the relevant date and assign a PM for this procurement."},
    {"no": 2, "name": "Please prepare and update proposal request form. Request and gather proposals from suppliers. Archive proposals and proformas digitally."},
    {"no": 3, "name": "Please check the digital archive. Submit the proposal comparison chart to PD for approval."},
    {"no": 4, "name": "Please prepare a Project Purchasement (PO)."},
    {"no": 5, "name": "Please review the contents of the PO and assign Project Purchasement (PO) number."},
    {"no": 6, "name": "Please have supplier sign on the Health and Safety Risk Analysis and Emergency Action Plans, which must be controlled sites with PO and Erginer Office Health and Safety Risk Analysis. Verify authorized signature. Have supplier sign on the On-Site Job Training Form."},
    {"no": 7, "name": "Please submit the PO to PD for approval signature."},
    {"no": 8, "name": "Please specify delivery of work time."},
    {"no": 9, "name": "Please review the PO. Pay in advance. If necessary, add to the checklist. In addition, please inform the accounting department about the advance payment with the PO number. Upload the advance payment receipt to this row."},
    {"no": 10, "name": "Please add the purchase and purchase schedule to PO list."},
    {"no": 11, "name": "Please check the PO and make the second payment due if necessary. Please also notify the accounting department about this second advance payment with the Project Purchasement Number (PO No)."},
    {"no": 12, "name": "Please request the consultant's ISO, TSE and CE documents, as well as their proficiency/accreditation and consent certificates. Please specify and check the consultant personnel's proficiency and training documents. Following that, if necessary, submit a request to the Finance Department for advance payment."},
    {"no": 13, "name": "Please request to the consultant for the documents specified by PM."},
    {"no": 14, "name": "Please ensure that all documents above have been archived as hard (wet ink) and soft copies."},
    {"no": 15, "name": "Please ensure that the invoice is issued correctly by supplier according to the attached sample. Additionally, please review the PO and invoice together."},
    {"no": 16, "name": "Please check the PO and make the remaining payment if necessary. Additionally, please inform the accounting department about the payment with the PO number."},
    {"no": 17, "name": "Please check the invoice of the exchange rate difference according to the payments made. If necessary, obtain approval from the PD to close the process accounting-wise by offsetting the payment or exchange difference invoices."},
    {"no": 18, "name": "Please make final checks of the entire process and obtain confirmation from the PD that the work has been completed."}
]

        try:
            PurchasementItem.objects.filter(purchasement_type=purchasement_type, project_type=1).delete()
            #	TRUNCATE TABLE purchasement_item RESTART IDENTITY CASCADE;

            # Verileri ekle, liste sırasına göre numara ata
            for idx, item in enumerate(data, start=1):  # idx sıralı numara olacak
                print(f"{item['no']}:{item['name']}")
                PurchasementItem.objects.create(
                    name=item['name'],
                    no=item['no'],  # Sıralı numara ekleniyor
                    purchasement_type_id=purchasement_type,
                    project_type_id=1
                )
        except Exception as ex:
            print(ex)
            return HttpResponse(f"PurchasementItem hata {str(ex)}!")

    return HttpResponse("PurchasementItem verileri başarıyla içe aktarıldı!")

 

@login_required(login_url = 'login')
def money(request):
    try:
        currencies = [
            {"name": "US Dollar", "short": "USD", "symbol": "$"},
            {"name": "Euro", "short": "EUR", "symbol": "€"},
            {"name": "British Pound", "short": "GBP", "symbol": "£"},
            {"name": "Turkish Lira", "short": "TRY", "symbol": "₺"},
        ]

        for currency in currencies:
            Money.objects.get_or_create(
                name=currency["name"],
                short=currency["short"],
                defaults={"symbol": currency["symbol"], "is_active": True}
            )
        print("Para birimleri başarıyla import edildi!")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    return HttpResponse("Ok")
 
@login_required(login_url='login')
def purchasement_type(request):
    try:
        purchase_process_types = [
            {"code_tr": "AFMK", "description_tr": "ALIŞ FATURALARI MAL KÜÇÜK", "code": "GS", "description": "GOODS SMALL"},
            {"code_tr": "AFMB", "description_tr": "ALIŞ FATURALARI MAL BÜYÜK", "code": "GB", "description": "GOODS BIG"},
            {"code_tr": "AFYK", "description_tr": "ALIŞ FATURALARI YAPIM KÜÇÜK", "code": "CS", "description": "CONSTRUCTION SMALL"},
            {"code_tr": "AFYB", "description_tr": "ALIŞ FATURALARI YAPIM BÜYÜK", "code": "CB", "description": "CONSTRUCTION BIG"},
            {"code_tr": "AFHİ", "description_tr": "ALIŞ FATURALARI HİZMET İŞÇİLİK", "code": "SL", "description": "SERVICE LABOUR"},
            {"code_tr": "AFHD", "description_tr": "ALIŞ FATURALARI HİZMET DANIŞMANLIK", "code": "SC", "description": "SERVICE CONSULTANCY"},
        ]

        for process in purchase_process_types:
            obj, created = PurchasementType.objects.get_or_create(
                code=process["code"],
                defaults={
                    "description": process["description"],
                    "code_tr": process["code_tr"],
                    "description": process["description"]
                }
            )
            if created:
                print(f"Yeni kayıt oluşturuldu: {obj}")
            else:
                print(f"Bu kayıt zaten mevcut: {obj}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return HttpResponse(f"Bir hata oluştu: {e}")

    return HttpResponse("Kayıt işlemi tamamlandı.")




@login_required(login_url = 'login')
def import_purchasement_steps(request):
        # Önce tüm kayıtları sil
    PurchasementStep.objects.all().delete()
    # Sabit veri GSesi
    data = [
        {"NO": 1, "ITEMS": "PV MODULE & CONNECTOR", "PURCH_TYPE": "GB"},
        {"NO": 2, "ITEMS": "SOLAR CABLE", "PURCH_TYPE": "GB"},
        {"NO": 3, "ITEMS": "INVERTER", "PURCH_TYPE": "GB"},
        {"NO": 4, "ITEMS": "CONSTRUCTION MATERIAL (TRACKER)", "PURCH_TYPE": "GB"},
        {"NO": 5, "ITEMS": "CIVIL&ELECTRICAL WORKS", "PURCH_TYPE": "SL"},
        {"NO": 6, "ITEMS": "MV EQUIPMENTS FOR SPP", "PURCH_TYPE": "GB"},
        {"NO": 7, "ITEMS": "LV PANELS", "PURCH_TYPE": "GB"},
        {"NO": 8, "ITEMS": "CABLES", "PURCH_TYPE": "GS"},
        {"NO": 9, "ITEMS": "GRID CONNECTION (TURN-KEY)", "PURCH_TYPE": "CB"},
        {"NO": 10, "ITEMS": "FENCES", "PURCH_TYPE": "GS"},
        {"NO": 11, "ITEMS": "EARTHING & LIGHTINING EQUIPMENTS", "PURCH_TYPE": "GS"},
        {"NO": 12, "ITEMS": "FIRE EXTINGUISHING SYSTEM", "PURCH_TYPE": "CS"},
        {"NO": 13, "ITEMS": "LOGERG & GUARDIAN 3.0 & DRON", "PURCH_TYPE": "GS"},
        {"NO": 14, "ITEMS": "CCTV (AVAILABLE TO LOGERG)", "PURCH_TYPE": "CS"},
        {"NO": 15, "ITEMS": "ELECTRICAL EQUIPMENTS", "PURCH_TYPE": "GS"},
        {"NO": 16, "ITEMS": "VILLA (CONTAINERIZED) & SITE DEPOT", "PURCH_TYPE": "GB"},
        {"NO": 17, "ITEMS": "LANDSCAPING WORKS", "PURCH_TYPE": "CB"},
        {"NO": 18, "ITEMS": "MANAGEMENT EXPENSES", "PURCH_TYPE": "GS"},
        {"NO": 19, "ITEMS": "CEMENT, SAND AND OTHER CIVIL GOODS", "PURCH_TYPE": "GS"},
        {"NO": 20, "ITEMS": "MAP ENGINEERING", "PURCH_TYPE": "SC"},
        {"NO": 21, "ITEMS": "CONSULTANTS (PWC, CUSTOM CONS., PV MODULE INSPECTOR. COMM. SUPERVISOR)", "PURCH_TYPE": "GS"},
        {"NO": 22, "ITEMS": "TAXES AND FEES FOR CONSTRUCTION AND CUSTOM DUTIES", "PURCH_TYPE": "GS"},
        {"NO": 23, "ITEMS": "ALL RISK INSURANCE", "PURCH_TYPE": "SC"},
        {"NO": 24, "ITEMS": "LOGISTICS (REGIONAL COMPANY)", "PURCH_TYPE": "SL"},
        {"NO": 25, "ITEMS": "INTERNATIONAL LOGISTICS", "PURCH_TYPE": "SL"},
        {"NO": 26, "ITEMS": "CUSTOMS WAREHOUSE", "PURCH_TYPE": "SC"},
        {"NO": 27, "ITEMS": "OTHERS (ADDITIONAL INSURANCE, OTHER SITE NEEDS)", "PURCH_TYPE": "GS"},
    ]
    
    # project_type_id sabit
    project_type_id = 1
    
    for row in data:
        try:
            # PurchasementType'i çek
            purchasement_type = PurchasementType.objects.get(code=row['PURCH_TYPE'])
        except PurchasementType.DoesNotExist:
            return HttpResponse(f"PurchasementType '{row['PURCH_TYPE']}' bulunamadı.", status=400)
        
        # Model kaydı
        PurchasementStep.objects.create(
            name=row['ITEMS'],
            no=row['NO'],
            purchasement_type=purchasement_type,
            project_type_id=project_type_id
        )
    
    return HttpResponse("Tüm PurchasementStep kayıtları başarıyla eklendi.")


 
@login_required(login_url = 'login') 
def import_cost_items(request):
    try:
        # Tablodaki veriler
        data = [
    {
        "number": 1,
        "name": "PV MODULE & CONNECTOR",
        "purchase_type": "GB",
        "made_in": "PRC",
        "supplier": "JINKO",
        "producer": "JINKO",
        "customs_required": "YES",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 2,
        "name": "SOLAR CABLE",
        "purchase_type": "GB",
        "made_in": "TR",
        "supplier": "EGE KABLO",
        "producer": "EGE KABLO",
        "customs_required": "YES",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 3,
        "name": "INVERTER",
        "purchase_type": "GB",
        "made_in": "PRC",
        "supplier": "HUAWEI",
        "producer": "HUAWEI",
        "customs_required": "YES",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 4,
        "name": "CONSTRUCTION MATERIAL (TRACKER)",
        "purchase_type": "GB",
        "made_in": "TR OR PRC",
        "supplier": "SCHLETTER",
        "producer": "SCHLETTER",
        "customs_required": "YES",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 5,
        "name": "CIVIL&ELECTRICAL WORKS",
        "purchase_type": "SL",
        "made_in": "EU",
        "supplier": "EASTERN EUROPEAN COMPANIES",
        "producer": "EASTERN EUROPEAN COMPANIES",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 6,
        "name": "MV EQUIPMENTS FOR SPP",
        "purchase_type": "GB",
        "made_in": "TR",
        "supplier": "ERGINER",
        "producer": "ORMAZABAL, RTS PREFABRIC, ELTAŞ",
        "customs_required": "?",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": "İHRAÇ KAYITLI | İTALYAN ŞİRKET DE ARAYALIM"
    },
    {
        "number": 7,
        "name": "LV PANELS",
        "purchase_type": "GB",
        "made_in": "TR",
        "supplier": "TEKPAN",
        "producer": "TEKPAN",
        "customs_required": "YES",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 8,
        "name": "CABLES",
        "purchase_type": "GS",
        "made_in": "TR",
        "supplier": "ÖZNUR (ERGİNER)",
        "producer": "ÖZNUR PYRISMIAN(COM. CABLE)",
        "customs_required": "YES",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": "İHRAÇ KAYITLI"
    },
    {
        "number": 9,
        "name": "GRID CONNECTION (TURN-KEY)",
        "purchase_type": "CB",
        "made_in": "-",
        "supplier": "ITALIAN COMPANY",
        "producer": "ITALIAN COMPANY",
        "customs_required": "",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": "MV CABLES EXCLUDED | MV SWITCHGEARS INCLUDED | TERNA&ENEL SCADA INCLUDED"
    },
    {
        "number": 10,
        "name": "FENCES",
        "purchase_type": "GS (CS)",
        "made_in": "ITA OR TR",
        "supplier": "ITALIAN COMPANY",
        "producer": "ITALIAN COMPANY",
        "customs_required": "",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 11,
        "name": "EARTHING & LIGHTINING EQUIPMENTS",
        "purchase_type": "GS",
        "made_in": "TR",
        "supplier": "ERGINER",
        "producer": "RADSAN",
        "customs_required": "YES",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": "İHRAÇ KAYITLI"
    },
    {
        "number": 12,
        "name": "FIRE EXTINGUISHING SYSTEM",
        "purchase_type": "CS",
        "made_in": "ITA",
        "supplier": "ITALIAN COMPANY",
        "producer": "ITALIAN COMPANY",
        "customs_required": "",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 13,
        "name": "LOGERG & GUARDIAN 3.0 & DRON",
        "purchase_type": "GS",
        "made_in": "TR",
        "supplier": "ERGINER",
        "producer": "EU COMPANIES",
        "customs_required": "?",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": "DIŞ TİCARET UZMANI İLE GÖRÜŞÜLECEK."
    },
    {
        "number": 14,
        "name": "CCTV (AVAILABLE TO LOGERG)",
        "purchase_type": "CS",
        "made_in": "TR",
        "supplier": "ERGINER",
        "producer": "?",
        "customs_required": "?",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": "DİREKT ALINABİLECEK FİRMALAR ARAŞTIRILACAK."
    },
    {
        "number": 15,
        "name": "ELECTRICAL EQUIPMENTS",
        "purchase_type": "GS",
        "made_in": "TR",
        "supplier": "ITALIAN COMPANY",
        "producer": "ITALIAN COMPANY",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": "BAŞLIK, PABUÇ, MAKARON (ETC)"
    },
    {
        "number": 16,
        "name": "VILLA (CONTAINERIZED) & SITE DEPOT",
        "purchase_type": "GB",
        "made_in": "TR",
        "supplier": "ERGINER",
        "producer": "ERGINER",
        "customs_required": "YES",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 17,
        "name": "LANDSCAPING WORKS",
        "purchase_type": "CB",
        "made_in": "ITA",
        "supplier": "ITALIAN COMPANY",
        "producer": "ITALIAN COMPANY",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 18,
        "name": "MANAGEMENT EXPENSES",
        "purchase_type": "GS",
        "made_in": "ITA",
        "supplier": "SPV",
        "producer": "SPV",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 19,
        "name": "CEMENT, SAND AND OTHER CIVIL GOODS",
        "purchase_type": "GS",
        "made_in": "ITA",
        "supplier": "ITALIAN COMPANY",
        "producer": "ITALIAN COMPANY",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 20,
        "name": "MAP ENGINEERING",
        "purchase_type": "SC",
        "made_in": "ITA",
        "supplier": "ITALIAN COMPANY",
        "producer": "ITALIAN COMPANY",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 21,
        "name": "CONSULTANTS (PWC, CUSTOM CONS., PV MODULE INSPECTOR. COMM. SUPERVISOR)",
        "purchase_type": "GS",
        "made_in": "-",
        "supplier": "INTERNATIONAL COMPANIES",
        "producer": "INTERNATIONAL COMPANIES",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 22,
        "name": "TAXES AND FEES FOR CONSTRUCTION AND CUSTOM DUTIES",
        "purchase_type": "GS",
        "made_in": "ITA",
        "supplier": "SPV",
        "producer": "SPV",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 24,
        "name": "ALL RISK INSURANCE",
        "purchase_type": "SC",
        "made_in": "ITA",
        "supplier": "PWC",
        "producer": "-",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 25,
        "name": "LOGISTICS (REGIONAL COMPANY)",
        "purchase_type": "SL",
        "made_in": "ITA",
        "supplier": "",
        "producer": "",
        "customs_required": "",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 26,
        "name": "INTERNATIONAL LOGISTICS",
        "purchase_type": "SL",
        "made_in": "EU",
        "supplier": "",
        "producer": "",
        "customs_required": "",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    },
    {
        "number": 27,
        "name": "OTHERS (ADDITIONAL INSURANCE, OTHER SITE NEEDS)",
        "purchase_type": "GS",
        "made_in": "ITA",
        "supplier": "ITALIAN COMPANY",
        "producer": "ITALIAN COMPANY",
        "customs_required": "NO",
        "pa": "",
        "pm": "",
        "pd": "",
        "notes": ""
    }
]

        project=Project.objects.filter(type__name="Solar Power Plant")
        owner = Project.owner_id
        # Verileri işleme ve kaydetme
        for item in data:
            try:
                purchasement_step = PurchasementStep.objects.get(name=item["name"])
                
                # Boole değerine çevrim
                customs_required = item["customs_required"].upper() == "YES"
                
                PurchasementStepDetail.objects.create(
                    project=project,  # Default bir proje kullanabilirsiniz
                    purchasement_step=purchasement_step,
                    purchasement_type=item["purchase_type"],
                    name=item["name"],
                    number=item["number"],
                    description=item.get("description", ""),
                    made_in=item.get("made_in", ""),
                    supplier=item.get("supplier", ""),
                    producer_brand=item.get("producer", ""),
                    customs_required=customs_required,
                    pa_id = Account.objects.filter(name=item["pa"]).first(),
                    pm=None if not item["pm"] else Account.objects.filter(name=item["pm"]).first(),
                    pd=None if not item["pd"] else Account.objects.filter(name=item["pd"]).first(),
                    notes=item.get("notes", ""),
                    currency=Money.objects.first()  # Varsayılan bir para birimi alınabilir
                )
            except PurchasementStep.DoesNotExist:
                return HttpResponse(f"PurchasementStep '{item['name']}' not found.", status=404)
            except Exception as e:
                return HttpResponse(f"Error processing item {item['name']}: {str(e)}", status=500)

        return HttpResponse("Cost items imported successfully.", status=200)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
