from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from numpy import product
 
from common.models import Money
from company.models import Company
from purchasement.models import CostItem, PurchasementItem

from account.models import UserAuth, UserProfile
import os, pandas as pd
from django.contrib import messages, auth
from django.db.models.functions import Cast, Coalesce, TruncDate
from django.db.models import Count, TextField, F, Sum,Max,Q
from django.db.models import FloatField, TextField

from purchasement.models import PurchasementStep, PurchasementType
from project.models import ProjectType
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
        {"name_tr": "MAL ALIMINI TANIMLA, İLK TARİHİ GİR VE İLGİLİ İŞ İÇİN PM ATAMASINI YAP VE AFMK UYARISI VER", 
        "name": "DEFINING PRODUCT PURCHASE, SPECIFYING START DATE, ASSIGNING PM, GIVING GS ALERT"},
        {"name_tr": "TEKLİF TALEP FORMU HAZIRLA GELEN TEKLİFLERİ VE PROFORMALARI DİJİTAL OLARAK ARŞİVLE", 
        "name": "PREPARING PROPOSAL REQUEST FORM, ARCHIVING PROPOSALS AND PROFORMAS AS DIGITAL"},
        {"name_tr": "DİJİTAL ARŞİVİ KONTROL ET VE TEKLİF KARŞILAŞTIRMA TABLOSUNU PM DENETİMİNDE MD ONAYINA SUN.", 
        "name": "CONTROLLING OF THE DIGITAL ARCHIVE, SUBMITTING COMPARISON CHART TO MD FOR APPROVAL AFTER CHECKING THE DOCUMENTS WITH PM"},
        {"name_tr": "PO (SİPARİŞ EMRİ) HAZIRLA PO'YU VE ONAYLI FORMU QPE'YE TESLİM ET", 
        "name": "PREPARING PO (PURCHASE ORDER), DELIVERING THE PO AND APPROVED FORM TO QPE"},
        {"name_tr": "PO (SİP. EMRİ) İÇERİK KONT. YAP PO ve PROJE NO ATA PO'YU TEDARİKÇİYE İMZALAT VE MD'NİN ONAYINA SUN", 
        "name": "CHECKING THE PO IN TERMS OF SUBSTANCE, ASSIGNING THE PO NUMBER AND PROJECT NUMBER, HAVING SUPPLIER SIGN ON THE PO, SUBMITTING THE PO TO MD FOR APPROVE"},
        {"name_tr": "PO'YU KONTROL ET VE AVANS ÖDEMESİNİ YAP VE GEREKLİ İSE ÇEK LİSTESİNE EKLE. YAPTIĞIN ÖDEMEYİ MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CHECKING THE PO, MAKING ADVANCE PAYMENT AND ATTACHING CHECK LIST IF IS REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE ADVANCE PAYMENT WITH THE PO NUMBER"},
        {"name_tr": "SİPARİŞİ PO LIST'E EKLE", 
        "name": "ADDING THE PURCHASEMENT TO PO LIST"},
        {"name_tr": "MALZEME TESLİME HAZIRDIR BİLDİRİMİNİ AL VE TESLİMATI ORGANİZE ET GEREKLİ İSE İKİNCİ ÖDEMEYİ MD'DEN TALEP ET", 
        "name": "AFTER PRODUCTS IS READY ORGANIZING THE DELIVERY, REQUESTING THE SECOND PAYMENTS FROM MD IF REQUIRED"},
        {"name_tr": "SÖZLEŞMEYİ KONTROL ET VE VARSA İKİNCİ AVANS VEYA KALAN ÖDEMEYİ YAP. YAPTIĞIN ÖDEMEYİ MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CONTROLLING THE CONTRACT, MAKING OTHER ADVANCE OR REMAINED PAYMENT IF REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE PAYMENT WITH THE PO NUMBER"},
        {"name_tr": "MALLARI EKSİKSİZ TESLİM AL. AKSİ DURUMDA ÇÖZÜMÜ İÇİN TEDARİKÇİ VE YÖNETİCİNDEN DESTEK İSTEYEBİLİRSİN. İRSALİYE VE FOTOĞRAF HAZIRLA VE EVRAKLARI BURAYA YÜKLE", 
        "name": "RECEIVING PRODUCTS IN FULL, GETTING SUPPORT FROM SUPPLIER OR RELEVANT MANAGER IF REQUIRED, PREPARING WAYBILL AND PHOTOS AND UPLOADING DOCUMENTS IN THIS ROW"},
        {"name_tr": "PM'DEN GELEN EVRAKLARI İNCELE VE KLASÖRLE (HARD&SOFT)", 
        "name": "EXAMINING AND FILING DOCUMENTS (AS HARD AND SOFT) THAT COME FROM PM"},
        {"name_tr": "SÜREÇ TAKİBİ VE FATURANIN TEDARİKÇİ TARAFINDAN DOĞRU ŞEKİLDE KESİLDİĞİNE EMİN OL", 
        "name": "MONITORING THE PROCESS AND ENSURING THAT INVOICE IS CORRECTLY ISSUED BY SUPPLIER"},
        {"name_tr": "FATURAYI PO'YA GÖRE KONTROL ET VE KABUL ET TARAMA YAP SOFT COPY OLARAK BULUTA KAYDET", 
        "name": "CHECKING THE INVOICE IN ACCORDANCE WITH THE PO AND ACCEPTING THE INVOICE, SCANNING THE PO AND UPLOADING TO CLOUD AS SOFT COPY"},
        {"name_tr": "PO'YU KONTROL ET VE VARSA KALAN ÖDEMEYİ YAP. YAPTIĞIN ÖDEMEYİ VE FATURALARI MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CHECKING THE PO AND MAKING REMAINING PAYMENT IF REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE PAYMENT AND INVOICES WITH THE PO NUMBER"},
        {"name_tr": "VARSA KALAN ÖDEMEYİ YAP, YAPILAN ÖDEMELERE GÖRE KUR FARKI FATURASI KONTROLÜNÜ YAP ve MD'DEN ONAY AL", 
        "name": "MAKING REMAINING PAYMENT IF REQUIRED, CHECKING EXCHANGE DIFFERENCE INVOICE IN ACCORDANCE WITH PAYMENTS AND RECEIVING APPROVAL FROM MD"},
        {"name_tr": "SON KONTROLLERİ YAP VE İŞİN TAMAMLANDIĞINA DAİR MD'DEN ONAY AL", 
        "name": "MAKING LAST CONTROLLS, RECEIVING APPROVAL RELATED TO COMPLETING THE WORKS FROM MD"}
    ]

        elif purchasement_type == 2: #	GB
            data = [
        {"name_tr": "MAL ALIMINI TANIMLA, İLK TARİHİ GİR VE İLGİLİ İŞ İÇİN PM ATAMASINI YAP VE AFMB UYARISI VER", 
        "name": "DEFINING PRODUCT PURCHASE, SPECIFYING START DATE, ASSIGNING PM, GIVING GB ALERT"},
        {"name_tr": "HAZIR ŞARTNAMEYİ AL VE ÖZEL ŞARTLAR BÖLÜMÜNÜ GÜNCELLE", 
        "name": "PREPARING THE ALREADY CREATED REGULATION AND UPDATING SPECIAL TERMS ACCORDING TO PROJECT"},
        {"name_tr": "TEKLİF TALEP FORMU HAZIRLA VE TEKLİFLERİ ŞARTNAME ONAYLARI İLE TEMİN ET GELEN TEKLİFLERİ VE PROFORMALARI DİJİTAL OLARAK ARŞİVLE", 
        "name": "PREPARING PROPOSAL REQUEST FORM AND COLLECTING THE PROPOSALS WITH APPROVED REGULATIONS ARCHIVING PROPOSALS AND PROFORMAS AS DIGITAL"},
        {"name_tr": "HAZIR SÖZLEŞMEYİ AL, SARI İLE BOYALI KISIMLARI GÜNCELLE VE GEREKLİ İSE AVUKATLA GÖRÜŞÜP İMZAYA HAZIR HALİNİ BURAYA EKLE", 
        "name": "PREPARING THE ALREADY CREATED CONTRACT AND UPDATING PLACES THAT PAINTED AS YELLOW ACCORDING TO PROJECT ATTACHING THE CONTRACT AS READY TO SIGN AFTER CONSULT ON THE LAWYER IF REQUIRED"},
        {"name_tr": "DİJİTAL ARŞİVİ KONTROL ET VE TEKLİF KARŞILAŞTIRMA TABLOSUNU PM DENETİMİNDE MD ONAYINA SUN.", 
        "name": "CONTROLLING OF THE DIGITAL ARCHIVE, SUBMITTING COMPARISON CHART TO MD FOR APPROVAL AFTER CHECKING THE DOCUMENTS WITH PM"},
        {"name_tr": "SÖZLEŞME İÇERİK KONTROLÜ YAP VE PO NO ATAMA + TEDARİKÇİYE İMZALATINCA MD ONAYINA SUN.", 
        "name": "CONTROLLING OF THE CONTACT BY MEANS OF CONTENT AND ASSIGNING PO (PURCHASE ORDER), SUBMITTING THE CONTRACT TO MD FOR APPROVAL AFTER HAVING SUPPLIER SIGN ON THE CONTRACT"},
        {"name_tr": "SÖZLEŞMEYİ İNCELE VE UYGUNSA İMZALA", 
        "name": "EXAMINING THE CONTRACT AND SIGNING"},
        {"name_tr": "SÖZLEŞMEYİ KONTROL ET VE AVANS ÖDEMESİNİ YAP VE GEREKLİ İSE ÇEK LİSTESİNE EKLE. YAPTIĞIN ÖDEMEYİ MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CHECKING THE CONTRACT AND MAKING ADVANCE PAYMENT, ADDING ON THE CHECK-LIST IF REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE ADVANCE PAYMENT WITH THE PO NUMBER"},
        {"name_tr": "SİPARİŞİ PO LIST'E EKLE", 
        "name": "ADDING THE PURCHASEMENT TO PO LIST"},
        {"name_tr": "MALZEME TESLİME HAZIRDIR BİLDİRİMİNİ AL VE TESLİMATI ORGANİZE ET GEREKLİ İSE İKİNCİ ÖDEMEYİ MD'DEN TALEP ET", 
        "name": "AFTER PRODUCTS IS READY ORGANIZING THE DELIVERY, REQUESTING THE SECOND PAYMENTS FROM MD IF REQUIRED"},
        {"name_tr": "SÖZLEŞMEYİ KONTROL ET VE VARSA İKİNCİ AVANS VEYA KALAN ÖDEMEYİ YAP. YAPTIĞIN ÖDEMEYİ MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CONTROLLING THE CONTRACT, MAKING OTHER ADVANCE OR REMAINED PAYMENT IF REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE PAYMENT WITH THE PO NUMBER"},
        {"name_tr": "FAT TALEP ET.FAT YAPILMAYACAK İSE TEST DÖKÜMANLARINI VE MALZEMENİN KİMLİĞİ VEYA SERİTİFKASINI İSTE.", 
        "name": "REQUESTING FAT (FACTORY ACCEPTANCE TEST). REQUESTING TEST DOCUMENTS, DATA-SHEETS AND CERTIFICATIONS IF FAT IS NOT REQUIRED"},
        {"name_tr": "FAT GEREKLİLİĞİ VE MÜŞTERİ KATILIMI GEREKLİLİĞİNİ DEĞERLENDİR", 
        "name": "EVALUATING REQUIREMENT OF FAT AND REQUIREMENT OF CUSTOMER ATTENDANCY TO THE FAT"},
        {"name_tr": "TESLİMAT TİPİNE GÖRE: TESLİMAT SONRASI İÇİN SİGORTA İŞLEMLERİNİ KONTROL ET (İNDİRME-YÜKLEME KAPSAMINI UNUTMA) EKSİKSE TAMAMLANMASI İÇİN QPE'YE İLET", 
        "name": "CONTROLLING OF INSURANCE OPERATIONS ACCORDING TO DELIVERY TYPE FOR AFTER TRANSPORTING (SCOPE OF LOADING AND UNLOADING IS ESSENTIAL) SENDING TO QPE FOR COMPLETING IF INCOMPLETE"},
        {"name_tr": "SİGORTA TALEBİNİ KONTROL ET VE MASTER SİGORTA LİSTESİ'Nİ KONTROL ET VE DURUMA GÖRE POLİÇEYE EKLET VEYA YENİ POLİÇE İÇİN İKİ TEKLİF ALIP ONAYA SUN", 
        "name": "CONTROLLING OF INSURANCE REQUEST AND MASTER INSURANCE LIST, ADDING TO INSURANCE POLICY IF REQUIRED OR GETTING TWO PROPOSALS FOR NEW INSURANCE POLICY AND SUBMITTING PROPOSALS TO MANAGER FOR APPROVE"},
        {"name_tr": "MALLARI EKSİKSİZ TESLİM AL. AKSİ DURUMDA ÇÖZÜMÜ İÇİN TEDARİKÇİ VE YÖNETİCİNDEN DESTEK İSTEYEBİLİRSİN. İRSALİYE VE FOTOĞRAF HAZIRLA VE EVRAKLARI BURAYA YÜKLE", 
        "name": "RECEIVING PRODUCTS IN FULL, GETTING SUPPORT FROM SUPPLIER OR RELEVANT MANAGER IF REQUIRED, PREPARING WAYBILL AND PHOTOS AND UPLOADING DOCUMENTS IN THIS ROW"},
        {"name_tr": "PM'DEN GELEN EVRAKLARI İNCELE VE KLASÖRLE (HARD&SOFT)", 
        "name": "EXAMINING AND FILING DOCUMENTS (AS HARD AND SOFT) THAT COME FROM PM"},
        {"name_tr": "SAT VEYA MAL TESLİM TUTANAĞI FORMUNU DOLDUR. İMZALA VE SÖZLEŞMEDE VAR İSE TEDARİKÇİYE İMZALAT", 
        "name": "PREPARING SAT(SITE ACCEPTANCE TEST) OR DELIVERY OF WORK RECORD FORM AND SIGNING, HAVING SUPPLIER SIGN ON THE DELIVERY OF WORK RECORD IF THE CONTRACT REQUIRES"},
        {"name_tr": "YUKARIDAKİ TÜM EVRAK VE FOTOLARI HARD COPY OLARAK KLASÖRLEDİĞİNİN KONTROLÜNÜ YAP", 
        "name": "CONTROLLING THAT ALL PREVIOUNS DOCUMETS AND PHOTOS ARE MADE IN FOLDER AS HARD COPY"},
        {"name_tr": "FATURAYI PO'YA GÖRE KONTROL ET VE KABUL ET TARAMA YAP SOFT COPY OLARAK BULUTA KAYDET", 
        "name": "CHECKING THE INVOICE IN ACCORDANCE WITH THE PO AND ACCEPTING THE INVOICE, SCANNING THE PO AND UPLOADING TO CLOUD AS SOFT COPY"},
        {"name_tr": "SON KONTROLLERİ YAP VE İŞİN TAMAMLANDIĞINA DAİR MD'DEN ONAY AL", 
        "name": "MAKING LAST CONTROLLS, RECEIVING APPROVAL RELATED TO COMPLETING THE WORKS FROM MD"}
    ]

        elif purchasement_type == 3: #CS bu eksik güncellenecek
            data = [
        {"name_tr": "HİZMET ALIMINI TANIMLA, İLK TARİHİ GİR VE İLGİLİ İŞ İÇİN PM ATAMASINI YAP", 
        "name": "DEFINING SERVICE PURCHASE, SPECIFYING START DATE, ASSIGNING PM"},
        {"name_tr": "HAZIR ŞARTNAMEYİ AL VE ÖZEL ŞARTLAR BÖLÜMÜNÜ GÜNCELLE", 
        "name": "PREPARING THE ALREADY CREATED REGULATION AND UPDATING SPECIAL TERMS ACCORDING TO PROJECT"},
        {"name_tr": "EKİBİNE BFÇ HAZIRLAT VE DENETLE", 
        "name": "BFÇ?"},]
        elif purchasement_type == 4: #CB
            data = [
        {"name_tr": "HİZMET ALIMINI TANIMLA, İLK TARİHİ GİR VE İLGİLİ İŞ İÇİN PM ATAMASINI YAP", 
        "name": "DEFINING SERVICE PURCHASE, SPECIFYING START DATE, ASSIGNING PM"},
        {"name_tr": "HAZIR ŞARTNAMEYİ AL VE ÖZEL ŞARTLAR BÖLÜMÜNÜ GÜNCELLE", 
        "name": "PREPARING THE ALREADY CREATED REGULATION AND UPDATING SPECIAL TERMS ACCORDING TO PROJECT"},
        {"name_tr": "EKİBİNE BFÇ HAZIRLAT VE DENETLE", 
        "name": "BFÇ?"},
        {"name_tr": "TEKLİF TALEP FORMU HAZIRLA GELEN TEKLİFLERİ VE PROFORMALARI DİJİTAL OLARAK ARŞİVLE", 
        "name": "PREPARING PROPOSAL REQUEST FORM, ARCHIVING PROPOSALS AND PROFORMAS AS DIGITAL"},
        {"name_tr": "DİJİTAL ARŞİVİ KONTROL ET VE TEKLİF KARŞILAŞTIRMA TABLOSUNU PM DENETİMİNDE MD ONAYINA SUN.", 
        "name": "CONTROLLING OF THE DIGITAL ARCHIVE, SUBMITTING COMPARISON CHART TO MD FOR APPROVAL AFTER CHECKING THE DOCUMENTS WITH PM"},
        {"name_tr": "HAZIR SÖZLEŞMEYİ AL VE SARI İLE BOYALI KISIMLARI GÜNCELLE", 
        "name": "PREPARING THE ALREADY CREATED CONTRACT AND UPDATING PLACES THAT PAINTED AS YELLOW ACCORDING TO PROJECT"},
        {"name_tr": "SÖZLEŞME İÇERİK KONT. PO NO ATA SÖZ. VE İSG ŞART.Nİ BELGEMİZİ TEDARİKÇİYE İMZALAT MD ONAYINA SUN", 
        "name": "CONTROLLING OF THE CONTACT BY MEANS OF THE CONTENT AND ASSIGNING PO (PURCHASE ORDER), HAVING SUPPLIER SIGN ON THE CONTRACT AND HSE (HEALTH AND SAFETY EXECUTIVE), SUBMITING THE CONTRACT AND HSE TO MD FOR APPROVAL"},
        {"name_tr": "İŞ TESLİM SÜRESİ", 
        "name": "DELIVERY OF WORK TIME"},
        {"name_tr": "SÖZLEŞMEYİ KONTROL ET VE AVANS ÖDEMESİNİ YAP VE GEREKLİ İSE ÇEK LİSTESİNE EKLE. YAPTIĞIN ÖDEMEYİ MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR. DEKONTU BURAYA YÜKLE", 
        "name": "CHECKING THE CONTRACT AND MAKING ADVANCE PAYMENT, ADDING ON THE CHECK-LIST IF REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE ADVANCE PAYMENT AND THE PO NUMBER UPLOADING THE ADVANCE PAYMENT RECEIPT TO THIS ROW"},
        {"name_tr": "SİPARİŞİ VE ÖDEME TAKVİMİNİ PO LIST'E EKLE", 
        "name": "ADDING THE PURCHASEMENT AND PURCHASEMENT SCHEDULE TO PO LIST"},
        {"name_tr": "FAT GEREKLİLİĞİ VE MÜŞTERİ KATILIMI GEREKLİLİĞİNİ DEĞERLENDİR", 
        "name": "EVALUATING REQUIREMENT OF FAT AND REQUIREMENT OF CUSTOMER ATTENDANCY TO THE FAT"},
        {"name_tr": "MD'DEN ONAY ALARAK FAT TALEP ET.FAT YAPILMAYACAK İSE TEST DÖKÜMANLARINI VE MALZEMENİN KİMLİĞİ VEYA SERİTİFKASINI İSTE. GEREKLİ İSE MÜŞTERİYİ DE DAVET ET. FAT BELGESİ İÇİN TEDARİKÇİNİN FORMU KULLANILACAK/YOKSA TEST DÖKÜMANI KARŞILIKLI İMZALANACAK.", 
        "name": "REQUESTING FAT (FACTORY ACCEPTANCE TEST) AFTER MD APPROVAL, REQUESTING TEST DOCUMENTS, DATA-SHEETS AND CERTIFICATIONS IF FAT IS NOT REQUIRED, SUPPLIER'S FAT FORM MUST BE USED. IF SUPPLIER DOESN'T HAVE THE ANY FAT FORM, FAT FORM MUST BE CREATED AND SIGNED MUTUALLY"},
        {"name_tr": "MALZEME HAZIRDIR BİLDİRİMİNİ PO'DAKİ VEYA SÖZLEŞMEDEKİ NAKLİYE SORUMLULUĞUNU KONTROL ET TEDARİKÇİ İLE GÖRÜŞÜP SİGORTALARI DA KONTROL EDEREK NAKLİYEYİ ORGANİZE ET", 
        "name": "CONTROLLING READINESS OF THE PRODUCTS, CONTROLLING STATEMENTS OF TRANSPORTATION ON THE PO OR CONTRACT, ORGANISING THE TRANSPORTATION AFTER CHECKING TRANSPORTATION STATEMENTS OF THE INSURANCE"},
        {"name_tr": "MALZEME SAHA TESLİMİ İRSALİYE VE FOTOĞRAF HAZIRLA VE EVRAKLARI QPE'YE İLET", 
        "name": "ORGANISING PRODUCTS DELIVERY TO SITE"},
        {"name_tr": "İŞÇİLİK/MONTAJ İÇİN SAHAYA GİTMEDEN EVVEL İSG ŞARTNAMESİ İÇİN GÖNDERİLEN EVRAKLARI KONTROL ET.", 
        "name": "CHECKING HSE DOCUMENTS THAT COME FROM THE SUPPLIER FOR HSE CONTRACT BEFORE STARTING SITE WORKS"},
        {"name_tr": "PM'DEN EVRAKLARI İSTE VE TAKİP ET SAHAYA GİRİLMEDEN EVVEL MUTLAKA AL. EĞER GELMEZ İSE MD'YE YAZILI OLARAK BİLDİR.", 
        "name": "ASKING THE DOCUMENTS FROM THE PM BEFORE STARTING THE SITE WORKS, THIS IS ESSENTIAL. IF DOCUMENTS ARE NOT CAME FROM PM, INFORMING THE MD BY TEXT"},
        {"name_tr": "İŞÇİLİK/MONTAJ SIRASINDA SAHADA GEREKLİ TEKNİK KONTROLLERİ YAP", 
        "name": "INSPECTING SITE INSTALLATION WORKS IN TERMS OF TECNICALLY"},
        {"name_tr": "SAT FORMUNU DOLDUR. İMZALA VE TEDARİKÇİYE İMZALAT", 
        "name": "FILLING, SIGNING AND HAVING SUPPLIER SIGN ON THE SAT (SITE ACCEPTANCE TEST) FORM"},
        {"name_tr": "YUKARIDAKİ TÜM EVRAK VE FOTOLARI HARD COPY OLARAK KLASÖRLEDİĞİNİN KONTROLÜNÜ YAP", 
        "name": "CONTROLLING THAT ALL PREVIOUS DOCUMENTS AND PHOTOS ARE MADE IN FOLDER AS HARD COPY"},
        {"name_tr": "SÜREÇ TAKİBİ VE FATURANIN TEDARİKÇİ TARAFINDAN DOĞRU ŞEKİLDE KESİLDİĞİNE EMİN OL", 
        "name": "MONITORING THE PROCESS AND ENSURING THAT INVOICE IS CORRECTLY ISSUED BY SUPPLIER"},
        {"name_tr": "YAPILAN ÖDEMELERE GÖRE KUR FARKI FATURASI KONTROLÜNÜ YAP ve MD'DEN ONAY AL", 
        "name": "CHECKING EXCHANGE DIFFERENCE INVOICE IN ACCORDANCE WITH PAYMENTS AND RECEIVING APPROVAL FROM MD"},
        {"name_tr": "SON KONTROLLERİ YAP VE İŞİN TAMAMLANDIĞINA DAİR MD'DEN ONAY AL", 
        "name": "MAKING LAST CONTROLLS, RECEIVING APPROVAL RELATED TO COMPLETING THE WORKS FROM MD"}
    ]

        elif purchasement_type == 5: #SL
            data = [
        {"name_tr": "HİZMET ALIMINI TANIMLA, İLK TARİHİ GİR VE İLGİLİ İŞ İÇİN PM ATAMASINI YAP", 
        "name": "DEFINING SERVICE PURCHASE, SPECIFYING START DATE, ASSIGNING PM"},
        {"name_tr": "TEKLİF TALEP FORMU HAZIRLA GELEN TEKLİFLERİ VE PROFORMALARI DİJİTAL OLARAK ARŞİVLE", 
        "name": "PREPARING PROPOSAL REQUEST FORM, ARCHIVING OFFERS AND PROFORMAS AS DIGITAL"},
        {"name_tr": "DİJİTAL ARŞİVİ KONTROL ET VE TEKLİF KARŞILAŞTIRMA TABLOSUNU PM DENETİMİNDE MD ONAYINA SUN.", 
        "name": "CONTROLLING OF DIGITAL ARCHIVE, SUBMITTING COMPARISON CHART TO MD FOR APPROVAL AFTER CHECKING THE DOCUMENTS WITH PM"},
        {"name_tr": "PO veya SÖZLEŞME HAZIRLA", 
        "name": "PREPARING PO (PURCHASE ORDER) OR CONTRACT"},
        {"name_tr": "PO İÇERİK KONTROLÜ PO NO ATA PO VE 'İSG ŞARTNAMESİ' BELGEMİZİ TEDARİKÇİYE İMZALAT", 
        "name": "CHECKING THE PO IN TERMS OF SUBSTANCE, ASSIGNING THE PO NUMBER AND PROJECT NUMBER, HAVING SUPPLIER SIGN ON THE PO AND HSE (HEALTH AND SAFETY EXECUTIVE)"},
        {"name_tr": "UYGUNSA PO VEYA SÖZLEŞME İMZALANACAK MD ONAYINA SUN.", 
        "name": "SUBMITTING AND SIGNING THE PO OR CONTRACT TO MD FOR APPROVAL"},
        {"name_tr": "İŞ TESLİM SÜRESİ", 
        "name": "DELIVERY OF WORK TIME"},
        {"name_tr": "SÖZLEŞMEYİ KONTROL ET VE AVANS ÖDEMESİNİ YAP VE GEREKLİ İSE ÇEK LİSTESİNE EKLE. YAPTIĞIN ÖDEMEYİ MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR. DEKONTU BURAYA YÜKLE", 
        "name": "CHECKING THE PO OR CONTRACT, MAKING ADVANCE PAYMENT AND ATTACHING CHECK LIST IF IS REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE ADVANCE PAYMENT WITH THE PO NUMBER UPLOADING THE PAYMENT RECEIPT TO THIS ROW"},
        {"name_tr": "SİPARİŞİ VE ÖDEME TAKVİMİNİ PO LIST'E EKLE", 
        "name": "ATTACHING THE PURCHASE AND THE PAYMENT SCHEDULE TO THE PO LIST"},
        {"name_tr": "İŞÇİLİK/MONTAJ İÇİN SAHAYA GİTMEDEN EVVEL 'İSG ŞARTNAMESİ' İÇİN GÖNDERİLEN EVRAKLARI KONTROL ET. İŞ BAŞI EĞİTİM FORMLARINI TALEP ET (TEDARİKÇİDEN) EĞER YOKSA TEDARİKÇİYE BİZİM FORMU İMZALAT. HERŞEY UYGUN İSE İŞE BAŞLAMA ONAYINI VER. İŞE BAŞLAMA ONAYI (İMZALI) UYGUN DEĞİL İSE İŞİ BAŞLATMAMA VEYA DURDURMA İLE İLGİLİ TÜM YETKİ VE SORUMLULUK SENDE.", 
        "name": "CHECKING HSE DOCUMENTS THAT COME FROM SERVICE&WORKMANSHIP SUPPLIER FOR HSE CONTRACT BEFORE STARTING SITE WORKS, REQUESTING ON-SITE-JOB TRAINING FORMS FROM THE SERVICE&WORKMANSHIP SUPPLIER, IF THE SUPPLIER DOESNT HAVE A FORM, HAVING SUPPLIER SIGN ON THE OUR ON-SITE-JOB TRAINING FORM (SIGNED), IF ALL DOCUMENTS AND PROGRESS ARE PROPER, APPROVING THE STARTING WORKS, IF NOT, DONT ALLOWING THE START, CEASING THE SITE WORKS"},
        {"name_tr": "PM'DEN EVRAKLARI İSTE VE TAKİP ET SAHAYA GİRİLMEDEN EVVEL MUTLAKA AL. EĞER GELMEZ İSE MD'YE YAZILI OLARAK BİLDİR. DOSYAYA İŞLE VE KLASÖRLE (HARD&SOFT).", 
        "name": "ASKING THE DOCUMENTS FROM THE PM BEFORE STARTING THE SITE WORKS, THIS IS ESSENTIAL. IF DOCUMENTS ARE NOT CAME FROM PM, INFORMING THE MD BY TEXT MAKING DOCUMENTS FILE IN A FOLDER AS HARD&SOFT"},
        {"name_tr": "İŞÇİLİK/MONTAJ SIRASINDA SAHADA GEREKLİ TEKNİK KONTROLLERİ YAP ATIK KABUL FORMLARINI TEDARİKÇİYE UYGULAT", 
        "name": "INSPECTING SITE INSTALLATION WORKS IN TERMS OF TECNICALLY, ENFORCING WASTE DISPOSAL RULES AND FORMS ON THE SITE"},
        {"name_tr": "İŞ BİTİMİNDE ATIK KABUL FORMLARINI PM'DEN TEMİN ET.", 
        "name": "ASKING THE WASTE DISPOSAL FORMS FROM THE PM AT COMPLETION OF WORKS"},
        {"name_tr": "İŞ TESLİM TUTANAĞI (KABUL)", 
        "name": "WORK DELIVERY RECORD (ACCEPTING)"},
        {"name_tr": "GELEN İŞ TESLİM TUTANAĞI VE EKLERİNİ TEK BİR .PDF OLARAK DÜZENLE VE SOFT HARD COPY OLARAK KLASÖRLE", 
        "name": "ARRANGING THE WORK DELIVERY RECORD AND ATTACHMENTS IN ONLY ONE .pdf FILE, MAKING DOCUMENTS FILE IN A FOLDER AS HARD&SOFT"},
        {"name_tr": "YUKARIDAKİ TÜM EVRAK VE FOTOLARI HARD COPY OLARAK KLASÖRLEDİĞİNİN KONTROLÜNÜ YAP", 
        "name": "CONTROLLING THAT ALL PREVIOUS DOCUMENTS AND PHOTOS ARE MADE IN FOLDER AS HARD COPY"},
        {"name_tr": "SÜREÇ TAKİBİ VE FATURANIN TEDARİKÇİ TARAFINDAN DOĞRU ŞEKİLDE KESİLDİĞİNE EMİN OL", 
        "name": "MONITORING THE PROCESS AND ENSURING THAT INVOICES ARE CORRECTLY CREATED BY THE SUPPLIER"},
        {"name_tr": "FATURAYI PO'YA GÖRE KONTROL ET VE KABUL ET TARAMA YAP SOFT COPY OLARAK BULUTA KAYDET VE VARSA KALAN ÖDEMEYİ YAP. YAPTIĞIN ÖDEMEYİ VE FATURALARI MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CHECKING AND ACCEPTING THE INVOICE ACCORDING TO PO, SCANNING THE DOCUMENTS, UPLOADING THE INVOICE AS SOFT COPY, MAKING PAYMENT IF THERE IS ANY REMAINING PAYMENT. INFORMING ACCOUNTING DEPARTMENT ABOUT THE PAYMENT AND INVOICES WITH THE PO NUMBER"},
        {"name_tr": "VARSA KALAN ÖDEMEYİ YAP, YAPILAN ÖDEMELERE GÖRE KUR FARKI FATURASI KONTROLÜNÜ YAP ve MD'DEN ONAY AL", 
        "name": "MAKING REMAINING PAYMENT IF REQUIRED, CHECKING EXCHANGE DIFFERENCE INVOICE IN ACCORDANCE WITH PAYMENTS AND RECEIVING APPROVAL FROM MD"},
        {"name_tr": "SON KONTROLLERİ YAP VE İŞİN TAMAMLANDIĞINA DAİR MD'DEN ONAY AL", 
        "name": "MAKING LAST CONTROLLS, RECEIVING APPROVAL RELATED TO COMPLETING THE WORKS FROM MD"}
    ]

        elif purchasement_type == 6: #1	SC
            data = [
        {"name_tr": "HİZMET ALIMINI TANIMLA, İLK TARİHİ GİR VE İLGİLİ İŞ İÇİN PM ATAMASINI YAP", 
        "name": "DEFINING SERVICE PURCHASE, SPECIFYING START DATE, ASSIGNING PM"},
        {"name_tr": "TEKLİF TALEP FORMU HAZIRLA GELEN TEKLİFLERİ VE PROFORMALARI QPE'YE İLET", 
        "name": "PREPARING PROPOSAL REQUEST FORM, ARCHIVING OFFERS AND PROFORMAS AS DIGITAL"},
        {"name_tr": "DİJİTAL ARŞİVİ KONTROL ET VE TEKLİF KARŞILAŞTIRMA TABLOSUNU PM DENETİMİNDE MD ONAYINA SUN.", 
        "name": "CONTROLLING OF DIGITAL ARCHIVE, SUBMITTING COMPARISON CHART TO MD FOR APPROVAL AFTER CHECKING THE DOCUMENTS WITH PM"},
        {"name_tr": "PO HAZIRLA", 
        "name": "PREPARING PO (PURCHASE ORDER)"},
        {"name_tr": "PO İÇERİK KONTROLÜ PO NO ATA", 
        "name": "CHECKING THE PO IN TERMS OF SUBSTANCE, ASSIGNING THE PO NUMBER AND PROJECT NUMBER"},
        {"name_tr": "PO VE ERGİNER OFİS İSG RİSK ANALİZİ İLE BERABER ZİYARETİ YAPILACAK SAHALARIN İSG RİSK ANALİZLERİNİ ve ACİL DURUM EYLEM PLANLARINI TEDARİKÇİYE İMZALAT (YETKİLİ İMZA KONTROLÜ YAP) VE İŞBAŞI EĞİTİM FORMUNU İMZALAT", 
        "name": "HAVING SUPPLIER SIGN ON THE HSE (HEALTH AND SAFETY EXECUTIVE) RISK ANALYSIS AND EMERGENCY ACTION PLAN WITH ERGINER OFFICE HSE RISK ANALYSIS, CHECKING AUTHORIZED SIGNATURE, HAVING SUPPLIER SIGN ON THE ON-SITE-JOB TRAINING FORM"},
        {"name_tr": "UYGUNSA PO VEYA SÖZLEŞME İMZALANACAK MD ONAYINA SUN.", 
        "name": "SUBMITTING AND SIGNING THE PO OR CONTRACT TO MD FOR APPROVAL"},
        {"name_tr": "İŞ TESLİM SÜRESİ", 
        "name": "DELIVERY OF WORK TIME"},
        {"name_tr": "PO'YU KONTROL ET VE AVANS ÖDEMESİNİ YAP VE GEREKLİ İSE ÇEK LİSTESİNE EKLE. YAPTIĞIN ÖDEMEYİ MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CHECKING THE PO, MAKING ADVANCE PAYMENT AND ATTACHING CHECK LIST IF IS REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE ADVANCE PAYMENT WITH THE PO NUMBER"},
        {"name_tr": "SİPARİŞİ VE ÖDEME TAKVİMİNİ PO LIST'E EKLE", 
        "name": "ATTACHING THE PURCHASE AND THE PAYMENT SCHEDULE TO THE PO LIST"},
        {"name_tr": "PO'YU VEYA SÖZLEŞMEYİ KONTROL ET VE VARSA İKİNCİ AVANS VEYA KALAN ÖDEMEYİ YAP. YAPTIĞIN ÖDEMEYİ MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CONTROLLING THE PO OR THE CONTRACT, MAKING OTHER ADVANCE OR REMAINED PAYMENT IF REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE PAYMENT WITH THE PO NUMBER"},
        {"name_tr": "FİRMANIN ISO, TSE VE CE BELGELERİNİ, YETKİNLİK / AKREDİTASYON VE İZİN BELGELERİNİ İSTE. HİZMET VERECEK PERSONELİN YETKİNLİK VE EĞİTİM BELGELERİNİ BELİRLE VE QPE'YE İLET VE GELENLERİ KONTROL ET. SONRASINDA AVANS ÖDEMESİ VAR İSE FİNANSTAN TALEP ET.", 
        "name": "REQUESTING CONSULTANT'S ISO, TSE AND CE DOCUMENTS, ALSO PROFICIENCY / ACCREDITATION AND CONSENT CERTIFICATES, SPECIFYING PROFICIENCY AND TRAINING DOCUMENTS AND SENDING TO QPE, CHECKING DOCUMENTS THAT COME FROM THE CONSULTANT, AFTER THAT, REQUESTING ADVANCE PAYMENT FROM FINANCE DEPARTMENT IF REQUIRED"},
        {"name_tr": "PM'İN BELİRLEDİĞİ EVRAKLARI TALEP ET. YUKARIDAKİ TÜM EVRAKLARI HARD VE SOFT COPY OLARAK KLASÖRLE.", 
        "name": "REQUESTING DOCUMENTS THAT SPECIFIED BY PM"},
        {"name_tr": "YUKARIDAKİ TÜM EVRAK VE FOTOLARI HARD COPY OLARAK KLASÖRLEDİĞİNİN KONTROLÜNÜ YAP", 
        "name": "CONTROLLING THAT ALL PREVIOUS DOCUMENTS AND PHOTOS ARE MADE IN FOLDER AS HARD COPY"},
        {"name_tr": "SÜREÇ TAKİBİ VE FATURANIN TEDARİKÇİ TARAFINDAN DOĞRU ŞEKİLDE KESİLDİĞİNE EMİN OL", 
        "name": "MONITORING THE PROCESS AND ENSURING THAT INVOICE IS CORRECTLY ISSUED BY SUPPLIER"},
        {"name_tr": "FATURAYI PO'YA GÖRE KONTROL ET VE KABUL ET TARAMA YAP SOFT COPY OLARAK BULUTA KAYDET", 
        "name": "CHECKING THE INVOICE IN ACCORDANCE WITH THE PO AND ACCEPTING THE INVOICE, SCANNING THE PO AND UPLOADING TO CLOUD AS SOFT COPY"},
        {"name_tr": "PO'YU KONTROL ET VE VARSA KALAN ÖDEMEYİ YAP. YAPTIĞIN ÖDEMEYİ VE FATURALARI MUHASEBEYE PO NO İLE BİRLİKTE BİLDİR", 
        "name": "CHECKING THE PO AND MAKING REMAINING PAYMENT IF REQUIRED, INFORMING ACCOUNTING DEPARTMENT ABOUT THE PAYMENT AND INVOICES WITH THE PO NUMBER"},
        {"name_tr": "VARSA KALAN ÖDEMEYİ YAP, YAPILAN ÖDEMELERE GÖRE KUR FARKI FATURASI KONTROLÜNÜ YAP ve MD'DEN ONAY AL", 
        "name": "MAKING REMAINING PAYMENT IF REQUIRED, CHECKING EXCHANGE DIFFERENCE INVOICE IN ACCORDANCE WITH PAYMENTS AND RECEIVING APPROVAL FROM MD"},
        {"name_tr": "SON KONTROLLERİ YAP VE İŞİN TAMAMLANDIĞINA DAİR MD'DEN ONAY AL", 
        "name": "MAKING LAST CONTROLLS, RECEIVING APPROVAL RELATED TO COMPLETING THE WORKS FROM MD"}
    ]
        try:
            PurchasementItem.objects.filter(purchasement_type=purchasement_type, project_type=1).delete()
            #	TRUNCATE TABLE purchasement_item RESTART IDENTITY CASCADE;

            # Verileri ekle, liste sırasına göre numara ata
            for idx, item in enumerate(data, start=1):  # idx sıralı numara olacak
                print(f"name:{item['name']}:{len(item['name'])} name_tr:{item['name_tr']}:{len(item['name_tr'])}")
                PurchasementItem.objects.create(
                    name=item['name'],
                    name_tr=item['name_tr'],
                    number=idx,  # Sıralı numara ekleniyor
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
 
@login_required(login_url = 'login')
def purchasement_type(request):
    try:
        purchase_process_types = [
            {"code": "AFMK", "description": "ALIŞ FATURALARI MAL KÜÇÜK", "code_en": "GS", "description_en": "GOODS SMALL"},
            {"code": "AFMB", "description": "ALIŞ FATURALARI MAL BÜYÜK", "code_en": "GB", "description_en": "GOODS BIG"},
            {"code": "AFYK", "description": "ALIŞ FATURALARI YAPIM KÜÇÜK", "code_en": "CS", "description_en": "CONSTRUCTION SMALL"},
            {"code": "AFYB", "description": "ALIŞ FATURALARI YAPIM BÜYÜK", "code_en": "CB", "description_en": "CONSTRUCTION BIG"},
            {"code": "AFHİ", "description": "ALIŞ FATURALARI HİZMET İŞÇİLİK", "code_en": "SL", "description_en": "SERVICE LABOUR"},
            {"code": "AFHD", "description": "ALIŞ FATURALARI HİZMET DANIŞMANLIK", "code_en": "SC", "description_en": "SERVICE CONSULTANCY"},
        ]

        for process in purchase_process_types:
            PurchasementType.objects.get_or_create(
                code=process["code"],
                description=process["description"],
                code_en=process["code_en"],
                description_en=process["description_en"]
            )
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    return HttpResponse("Ok")




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
        {"NO": 24, "ITEMS": "ALL RISK INSURANCE", "PURCH_TYPE": "SC"},
        {"NO": 25, "ITEMS": "LOGISTICS (REGIONAL COMPANY)", "PURCH_TYPE": "SL"},
        {"NO": 26, "ITEMS": "INTERNATIONAL LOGISTICS", "PURCH_TYPE": "SL"},
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
            number=row['NO'],
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


        # Verileri işleme ve kaydetme
        for item in data:
            try:
                purchasement_step = PurchasementStep.objects.get(name=item["name"])
                purchasement_type=PurchasementType.objects.get(name_en=item["purchase_type"],)
                CostItem.objects.create(
                    purchasement_step=purchasement_step,
                    purchase_type=purchasement_type,
                    number=item["number"]
                )
            except PurchasementStep.DoesNotExist:
                return HttpResponse(f"PurchasementStep '{item['name']}' not found.", status=404)

        return HttpResponse("Cost items imported successfully.", status=200)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)



# @login_required(login_url = 'login')
# def purchasement_type(request):
#     try:
#         print()
            

#     except Exception as e:
#         print(f"Bir hata oluştu: {e}")

#     return HttpResponse("Ok")

# @login_required(login_url = 'login')
# def purchasement_type(request):
#     try:
#         print()
            

#     except Exception as e:
#         print(f"Bir hata oluştu: {e}")

#     return HttpResponse("Ok")

# @login_required(login_url = 'login')
# def purchasement_type(request):
#     try:
#         print()
            

#     except Exception as e:
#         print(f"Bir hata oluştu: {e}")

#     return HttpResponse("Ok")
