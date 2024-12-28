from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Company
from project.models import ProjectType

#@login_required(login_url='login')
def new_project(request):
    try:
        # Filtrelenmiş veriler
        customer_list = list(Company.objects.filter(type_id=1).values('id', 'name'))
        project_type_list = list(ProjectType.objects.filter(is_active=True).values('id', 'name'))

        # JSON formatına çevrilecek veri
        data = {
            "companies": customer_list,
            "project_types": project_type_list
        }
        return JsonResponse(data, status=200)

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return JsonResponse({"error": "Bir hata oluştu"}, status=500)


# @login_required(login_url = 'login')
# def purchasing(request):
#     userprofile = UserProfile.objects.get(user=request.user)   
#     # if request.user.is_admin == False:
#     #     context = { 'userprofile': userprofile,  }
#     #     return render(request, '403.html', context)
    
#     company_list = Company.objects.all().filter(type_id=3).order_by("id")
#     print(company_list[0])
#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#     }
#     return render(request, 'companies/purchasing.html', context)

 


# @login_required(login_url = 'login')
# def logistic(request):
#     userprofile = UserProfile.objects.get(user=request.user)   
#     # if request.user.is_admin == False:
#     #     context = { 'userprofile': userprofile,  }
#     #     return render(request, '403.html', context)
    
#     company_list = Company.objects.all().filter(type_id=2, is_active=True)
    
#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#     }
#     return render(request, 'companies/lojistik.html', context)

# @login_required(login_url = 'login')
# def distributor(request):
#     userprofile = UserProfile.objects.get(user=request.user)   
#     # if request.user.is_admin == False:
#     #     context = { 'userprofile': userprofile,  }
#     #     return render(request, '403.html', context)
    
#     company_list = Company.objects.all().filter(type_id=4, is_active=True)
    
#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#     }
#     return render(request, 'companies/distributor.html', context)
 
# @login_required(login_url = 'login')
# def company_processes(request):
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="company_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

#     userprofile = UserProfile.objects.get(user=request.user)   
   
     
#     company_list = Company.objects.all().filter(is_active=True).exclude(type_id=1).order_by("id").values('id','name','address'
#     ,'city__name','phone','email')
    
#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#     }
#     return render(request, 'companies/company_processes.html', context)


# @login_required(login_url = 'login')
# def new_company(request):
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="company_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

#     userprofile = UserProfile.objects.get(user=request.user)   

#     if "POST" in request.method:
#         # for key,value in request.POST.items():
#         #     print (f'company.{key} = request.POST[\'{key}\']')
        
#         company = Company()
#         company.type_id = request.POST['type_id']
#         company.usage_type_id = request.POST['usage_type_id']
#         company.name = request.POST['name']
#         company.full_name = request.POST['full_name']
#         company.address = request.POST['address']
#         company.city_id = request.POST['city_id']
#         company.tax_place = request.POST['tax_place']
#         company.tax_number = request.POST['tax_number']
#         company.web_site = request.POST['web_site']
#         company.registration_no = request.POST['registration_no']
#         company.email = request.POST['email']
#         company.phone = request.POST['phone']
#         company.contact_name = request.POST['contact_name']
#         company.second_phone = request.POST['second_phone']
#         company.save()

#         Logs(site="new_company", text=str(company.name)+ " adlı firma eklendi.", type="Yeni Firma Kaydı."
#             , created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), record_id=company.id, user_info=request.user.first_name+" "+request.user.last_name).save() 

#         messages.success(request, "Yeni Kayıt Eklendi!")
         
#         return redirect('company_processes')
	    
        
 
   
#     company_list = Company.objects.filter(is_active=True).exclude(type__id =1) #company_owner
#     type_list = CompanyType.objects.filter(is_active=True).exclude(name="Firma Sahibi")
#     usage_type_list = UsageType.objects.filter(is_active=True)
#     city_list = City.objects.filter(is_active=True).values('id','name')
    
#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#         'type_list': type_list,
#         'usage_type_list': usage_type_list,
#         'city_list': city_list,
#     }
#     return render(request, 'companies/new.html', context)

# @login_required(login_url = 'login')
# def moneyrate(request):
#     userprofile = UserProfile.objects.get(user=request.user)  
#     date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     money_list = Money.objects.filter(is_active=True).exclude(id=1)
#     out_str = f'date:{date} <br>'  
#     print(request.user.id)
#     for money in money_list:
#         rate = MoneyRate()
#         rate.money_id = money.id
#         price = CurrencyRates().get_rate(str(money.short), 'TRY')
#         out_str += f'money:{money.short} price:{price} TRY <br>'
#         rate.price = price*1000000
#         rate.date = date
#         rate.save()
    
#     context = {
#         'userprofile': userprofile,
       
#     #'labels' : json.dumps(labels),    
    
#     }
#     return HttpResponse(out_str)

# @login_required(login_url = 'login')
# def add_new_info(request):
#     userprofile = UserProfile.objects.get(user=request.user) 
#     if request.user.is_admin == False:
#         context = {
#     'userprofile': userprofile,
#     }
#         return render(request, '403.html',context) 
#     try:

#         # try:
#         #     BuyingType.objects.get(name="Malzeme Ücreti")
#         # except BuyingType.DoesNotExist:
#         #     BuyingType(name="Malzeme Ücreti").save()
#         #     BuyingType(name="Nakliye Ücreti").save()
#         #     BuyingType(name="Diğer Ücretler").save()
            
           
        
#         try:
#             right = UserRight.objects.get(name='accounting')
#         except UserRight.DoesNotExist:
#             UserRight(name='accounting',description='Muhasebe Departmanı',mail_list='muhasebe,yonetim', is_approve=True).save()
            
        
#         try:
#             PurchasingStatus.objects.get(id=0)
#         except PurchasingStatus.DoesNotExist:
#             PurchasingStatus(name='Giriş Onayı Bekleniyor').save()
#             PurchasingStatus(name='Fiyat Onayı Bekleniyor').save()
#             PurchasingStatus(name='Onaylandı').save()
#             PurchasingStatus(name='İptal Edildi').save()
#             PurchasingStatus(name='Yönetici Onay Bekleniyor').save()
#             PurchasingStatus(name='Yönetici Onayladı').save()
#             PurchasingStatus(name='Yönetici İptal Etti').save()
            


#         try:
#             right = UserRight.objects.get(name='selling')
#         except UserRight.DoesNotExist:
#             UserRight(name='selling',description='Satış Departmanı',mail_list='satis,uretim,yonetim', is_approve=True).save()
#             #UserRight(name='selling_personel',description='Satış Uzmanı',mail_list='satis', is_approve=True).save()
#             UserRight(name='selling_manager',description='Satış Direktörü',mail_list='satis,uretim,yonetim', is_approve=True).save()

#         try:
#             right = UserRight.objects.get(name='purchasing_manager')
#         except UserRight.DoesNotExist:
#             UserRight(name='purchasing_manager',description='Satın Alma Müdürü',mail_list='satin_alma', is_approve=True).save()
            
#         try:
#             right = UserRight.objects.get(name='purchasing')
#         except UserRight.DoesNotExist:
            
#             UserRight(name='purchasing',description='Satın Alma Uzmanı',mail_list='satin_alma,uretim,yonetim', is_approve=True).save()
#         try:
#             right = UserRight.objects.get(name='logistic')
#         except UserRight.DoesNotExist:
            
#             UserRight(name='logistic',description='Lojistik',mail_list='lojistik,yonetim', is_approve=True).save()
#         try:
#             SellingStatus.objects.get(name="Teslim Edildi")
#         except SellingStatus.DoesNotExist:
#             SellingStatus(name="Onay Bekleniyor").save()
#             SellingStatus(name="Üretim Bekleniyor").save()
#             SellingStatus(name="Kargo Hazırlanıyor").save()
#             SellingStatus(name="Dağıtıma Çıktı").save()
#             SellingStatus(name="Teslim Edildi").save()
#             SellingStatus(name="İptal Edildi").save()
#             SellingStatus(name="Revize Edildi").save()
            
#         try:
#             print("started to chec palette_package_quantity ") 
#             product_count = Product.objects.filter(is_active=True, palette_package_quantity=1).count()
#             if product_count > 0:
#                 Product.objects.filter(is_active=True, palette_package_quantity=1).update(palette_package_quantity=F('palette_quantity') / F('package_quantity'))

#         except Exception as ex:
#             return HttpResponse(str(ex))

#     except Exception as ex:
#         return HttpResponse(str(ex))

#     return HttpResponse("BÜTÜN BİLGİLER KONTROL EDİLDİ")


# @login_required(login_url = 'login')
# def edit_company(request, id):
#     userprofile = UserProfile.objects.get(user=request.user)
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="company_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

    
#     try:
#         company = Company.objects.get(id=id)
#     except Exception as ex:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

#     if "POST" in request.method:
#         # for key,value in request.POST.items():
#         #     print (f'company.{key} = request.POST[\'{key}\']')
        
#         company.type_id = request.POST['type_id']
#         company.usage_type_id = request.POST['usage_type_id']
#         company.name = request.POST['name']
#         company.full_name = request.POST['full_name']
#         company.address = request.POST['address']
#         company.tax_place = request.POST['tax_place']
#         company.tax_number = request.POST['tax_number']
#         company.web_site = request.POST['web_site']
#         company.registration_no = request.POST['registration_no']
#         company.email = request.POST['email']
#         company.phone = request.POST['phone']
#         company.contact_name = request.POST['contact_name']
#         company.second_phone = request.POST['second_phone']
#         company.save()

#         Logs(site="edit_company", text=str(company.name)+ " adlı şirket bilgileri güncellendi.", type="Şirket Bilgileri Güncelleme."
#             , created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), record_id=company.id, user_info=request.user.first_name+" "+request.user.last_name).save() 

#         messages.success(request, company.name +" Şirket Bilgileri Güncellendi!")
         
#         return redirect('company_processes')
#     type_list = CompanyType.objects.filter(is_active=True).exclude(name="Firma Sahibi")
#     usage_type_list = UsageType.objects.filter(is_active=True)
#     city_list = City.objects.filter(is_active=True).values('id','name')
    
#     context = {
#         'userprofile': userprofile,
#         'company': company,
#         'type_list': type_list,
#         'usage_type_list': usage_type_list,
#         'city_list': city_list,
#     }
#     return render(request, 'companies/edit.html', context)
  

# @login_required(login_url = 'login')
# def delete_company(request):
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="company_processes")
#     except UserAuth.DoesNotExist:
#         userprofile = UserProfile.objects.get(user=request.user)
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)
    
#     url = request.META.get('HTTP_REFERER')
#     id = int(request.POST['company_id'])
#     if "GET" != request.method:
#         try:
#             company = Company.objects.get(id=id)
#         except Exception as ex:
#             context = {
#         'userprofile': userprofile,
#         }
#             return render(request, '403.html',context)
#         company.is_active = False
#         company.save()
#         messages.success(request, 'Kayıt Silindi.')
#         return redirect(url)
    

# @login_required(login_url = 'login')
# def save_selling_company_manuel(request):
#     """Bayi stok  bilgilerini excel dosyasından kayıt etme 
#     http://127.0.0.1:8000/companies/save_selling_company_manuel/"""
#     userprofile = UserProfile.objects.get(user=request.user)  
#     if request.user.is_admin == False:
#        context = { 'userprofile': userprofile,  }
#        return render(request, '403.html', context) 
   
#     date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     company_stock_list = []
#     all_company_stock_list = []
#     company_stock = {}
#     sheet_index= 0
#     if "POST" == request.method:
    
#         excel_file = request.FILES["excel"]
#         df = pd.DataFrame(excel_file)
    
#         df = pd.read_excel(io=excel_file, sheet_name=sheet_index, usecols=range(0,68))
#         df = df.where(df.notna(), "***")
#         # print(df.head())
#         # print(df) 
#         product_code = ""
#         for i, col in enumerate(df.itertuples(), 1):
#           #  print(i, col)
#             try:
#                 if i == 1:
#                     for s in range(10,44):
#                         name = str(col[s]).strip().encode('utf-8', 'ignore')
#                         name = name.decode('utf-8', 'ignore')
                        
#                         if " " in name:
#                             location = name[name.rfind(' '):].strip() 
#                             name = name[0:name.rfind(' ')].strip() 
#                             company_stock['name'] = name
#                             company_stock['location'] = location.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
#                             company_stock['index'] = s
#                             company_stock_list.append(company_stock)
#                             company_stock = {}
                            
#                         s += 1
#                 elif i == 2:
#                     for cs in company_stock_list:
#                         company_name = str(col[cs['index']]).strip().encode('utf-8', 'ignore').decode('utf-8', 'ignore')
#                         cs['company_name'] = company_name
#                 elif i >= 6:
#                     if i == 6:
#                         company_stock_list = sorted(company_stock_list, key=lambda x: x['index'])
#                         # for cs in company_stock_list:
#                         #     print(cs['name'],cs['company_name'],cs['index'])
#                     product_code = str(col[1]).strip()
#                     if not product_code.startswith('***'):
#                         product = Product.objects.get(code=product_code)
#                         package_quantity = int(str(col[4]).strip())
#                         price = float(str(col[5]).strip())
#                         discount = str(col[6]).strip()
#                         if product.package_quantity != package_quantity:
#                             product.package_quantity = package_quantity
#                         if product.price != price:
#                             product.price = price
#                         for cs in company_stock_list:
#                             new_cs = copy.deepcopy(cs)
#                             total_package_quantity = 0
#                             if not str(col[cs['index']]).strip().startswith('***'):
#                                 total_package_quantity = int(float(str(col[cs['index']]).strip()))
                          
#                             new_cs['price'] = price
#                             new_cs['discount'] = discount
#                             new_cs['product_id'] = product.id
#                             new_cs['product_name'] = product.name
#                             new_cs['product_code'] = product.code
#                             new_cs['total_package_quantity'] = total_package_quantity
#                             new_cs['total_price'] = float(total_package_quantity * package_quantity) * price

#                             if total_package_quantity > 0 :
#                                 all_company_stock_list.append(new_cs)



               
#             except Exception as ex:
#                 print(f'{i} {product_code} ex:{str(ex)} ')
#                 pass
        
#         all_company_stock_list = sorted(all_company_stock_list, key=lambda x: x['name'])
        
#         #for cs in all_company_stock_list:
#             # if str(new_cs['name']) == 'Serdar AVCI' and new_cs['total_package_quantity'] >0:
#             #     print(new_cs['name'],new_cs['company_name'],new_cs['product_code'],new_cs['total_package_quantity'])
#     #{'name': 'Garip İLDENİZ', 'location': 'ADANA', 'index': 17, 'company_name': 'SÖZ KOZMETİK', 'price': 39.13, 'discount': '0', 'product_id': 165, 
#     # 'product_name': 'Borline Active Plus Sıvı Deterjan 1700', 'product_code': 'SDET01', 'total_package_quantity': 0, 'total_price': 0.0}
#     locale.setlocale(locale.LC_ALL, "tr_TR.utf8")
#     name_list = []
#     #locale.setlocale(locale.LC_ALL, "en_US.utf8")
#     password_list = ['ESd18*df','aSEd92*df','SdT82*dE','SG72*dEf','aSd12*df','SEd62*TaF']
#     pass_index = 0
#     company_name_list = []
#     for cs in all_company_stock_list:
#         try:
#             new_user = None
#             company_name = str(cs['company_name'])
#             company = None
#             if company_name not in company_name_list:
#                 company_name_list.append(company_name)
#             try:
#                 company = Company.objects.get(name=company_name)
#             except Company.DoesNotExist:
#                 company = Company(name=company_name,full_name=company_name,address="*")
#                 city_name = str(cs['location']).capitalize()
#                 city = None
#                 try:
#                     city = City.objects.get(name=city_name)
#                 except City.DoesNotExist:
#                     city = City(name=city_name)
#                     city.save()
#                 company.city_id = city.id
#                 company.save()

#             cs['company_id'] = company.id
       
#             name_str = my_common.normalize_string(request,str(cs['name']).lower().strip())
#             email = name_str.replace(' ','.')+"@borline.com.tr"
#             email = my_common.normalize_string(request,email)
#             if "hüseyin.batu@borline.com.tr" in email:
#                 email = "huseyin.batu@borline.com.tr"
#             if "murat.karakoç@borline.com.tr" in email:
#                 email = "murat.karakoc@borline.com.tr"
#             email = email.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
#             if email not in name_list:
#                 name_list.append(email)
#                 name_str = str(cs['name']).strip()
#                 first_name,last_name = name_str.split(' ')
#                 password = password_list[pass_index]
#                 pass_index += 1
                
#                 print(first_name,last_name,email,password)
                
#                 try:
#                     new_user = Account.objects.get(email=email)
                  
#                 except Account.DoesNotExist:
#                     new_user = Account()
#                     new_user.email = email
#                     new_user.username = email
#                     new_user.first_name = first_name.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
#                     new_user.last_name = last_name.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
#                     new_user.set_password(password)
#                     new_user.is_active = True
#                     new_user.save()
#                     new_profile = UserProfile()
#                     new_profile.user = new_user
#                     new_profile.phone_number = "05"
#                     new_profile.save()
#                 try:
#                     user_auth = UserAuth.objects.get(user_id=new_user.id, right__name="selling")
#                 except UserAuth.DoesNotExist:
#                     right = UserRight.objects.get(name="selling")
#                     uauth = UserAuth(user=new_user,right=right)
#                     uauth.save()    
#             if new_user is None:
#                 new_user = Account.objects.get(email=email)  
#             cs['user_id'] = new_user.id

#         except Exception as ex:
#             print(f'{company_name} {str(ex)} ')
#     all_company_stock_list = sorted(all_company_stock_list, key=lambda x: x['company_id'])
#     cd = None
#     amount = 0.0
#     cost = 0.0

   
         
#     for cs in all_company_stock_list:
#         try:
# #{'name': 'Garip İLDENİZ', 'location': 'ADANA', 'index': 17, 'company_name': 'SÖZ KOZMETİK', 'price': 39.13, 'discount': '0', 'product_id': 165, 
# # 'product_name': 'Borline Active Plus Sıvı Deterjan 1700', 'product_code': 'SDET01', 'total_package_quantity': 0, 'total_price': 0.0}
#             ucs = None
#             try:
#                 ucs = UserCompanySelling.objects.get(user_id=int(cs['user_id']), company_id=int(cs['company_id']))
#             except UserCompanySelling.DoesNotExist:
#                 ucs = UserCompanySelling(user_id=int(cs['user_id']), company_id=int(cs['company_id']))
#                 ucs.save()

#             if cd is None:
#                 try:
#                     cd = CompanyDetails.objects.get(user_id=int(cs['user_id']), company_id=int(cs['company_id']))
#                 except CompanyDetails.DoesNotExist:
#                     cd = CompanyDetails(user_id=int(cs['user_id']), company_id=int(cs['company_id']))
#                     cd.created_at = date_str
#                     cd.status_id = 1 #Onay Bekleniyor 
#                     cd.save()
#             elif cd.company_id != cs['company_id']:
#                 cd.amount = round(amount,4)
#                 cd.cost = round(cost,4)
#                 cd.debt = round(amount,4)
#                 cd.save()
#                 cost = 0.0
#                 amount = 0.0
#                 try:
#                     cd = CompanyDetails.objects.get(user_id=int(cs['user_id']), company_id=int(cs['company_id']))
#                 except CompanyDetails.DoesNotExist:
#                     cd = CompanyDetails(user_id=int(cs['user_id']), company_id=int(cs['company_id']))
#                     cd.created_at = date_str
#                     cd.status_id = 1 #Onay Bekleniyor
#                     cd.save()
            
#             pde = None
#             try:
#                 pde = ProductDetails.objects.get(company_details_id=cd.id, product_id=int(cs['product_id']))
#             except ProductDetails.DoesNotExist:
#                 pde = ProductDetails(company_details_id=cd.id, product_id=int(cs['product_id']))
#                 pde.quantity = int(cs['total_package_quantity'])
#                 pde.price = round(float(cs['price']),4)
#                 pde.total_price = round(float(cs['total_price']),4)
#                 discount = 0
#                 if str(cs['discount']) not in '***':
#                     discount = int(cs['discount'])
#                 pde.discount = discount
#                 pde.created_at = date_str
#                 pde.total_cost = round(my_common.product_cost(request,pde.product_id,pde.quantity),3)
#                 stock_quantity = ProductStock.objects.filter(product_id=pde.product_id, status_id=1).aggregate(stock_quantity=Sum('quantity'))['stock_quantity'] #depodaki toplam ürünleri getir.
#                 if stock_quantity is not None and stock_quantity >= pde.quantity:
#                     pde.is_stock_available = True
                    
                
#                 amount += pde.total_price
#                 cost += pde.total_cost
#                 pde.save()
            
#         except Exception as ex:
#             print(f'{str(ex)} ')
#             print(f'{cs}')
            
    
#     if len(all_company_stock_list) > 0:
#         print(all_company_stock_list[0])
#     #{'name': 'Garip İLDENİZ', 'location': 'ADANA', 'index': 17, 'company_name': 'SÖZ KOZMETİK', 'price': 39.13, 'discount': '0', 'product_id': 165, 
#     # 'product_name': 'Borline Active Plus Sıvı Deterjan 1700', 'product_code': 'SDET01', 'total_package_quantity': 0, 'total_price': 0.0, 'company_id': 181}
#     context = {
#         'userprofile': userprofile,
        
#     }
#     return render(request, 'companies/save_selling_company_manuel.html', context)


# @login_required(login_url = 'login')
# def save_product_manuel(request):
#     """Ürünleri ve stok bilgilerini excel dosyasından kayıt etme 
#     http://127.0.0.1:8000/companies/save_product_manuel/"""
#     userprofile = UserProfile.objects.get(user=request.user)  
#     if request.user.is_admin == False:
#        context = { 'userprofile': userprofile,  }
#        return render(request, '403.html', context) 
   
#     date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     try:
#         Production.objects.all().delete()
#        # Product.objects.all().delete()
#     except Exception as ex:
#         print(str(ex))
#     if "POST" == request.method:
    
#         excel_file = request.FILES["excel"]
#         df = pd.DataFrame(excel_file)

#         sheet_index= 0
#         df = pd.read_excel(io=excel_file, sheet_name=sheet_index, usecols=range(0,18), skiprows=1)
#         df = df.where(df.notna(), "***")
#         print(df.head())
#         print(df) 
#         str_1 = "0"
#         for i, col in enumerate(df.itertuples(), 1):
#             print(i, col)
#             try:
#                 str_1 = str(col[1]).strip() 
#                 if not str_1.startswith('***'):
#                     try:
#                         product = Product.objects.get(code=str_1)
#                     except:
#                         product = Product()
#                         product.code = str_1

#                     product.name = str(col[2]).strip()
#                     product.description = str(col[3]).strip()

#                     type_name = str(col[4]).strip()
#                     try:
#                         usage_type = ProductType.objects.get(name=type_name)
#                     except:
#                         usage_type = ProductType(name=type_name)
#                         usage_type.save()
#                     if i == 4:
#                         print()
#                     product.type_id = usage_type.id
#                     product.meter = int(str(col[5]).strip())
#                     product.vat = float(str(col[6]).strip().replace(",","."))
#                     product.price = float(str(col[7]).strip().replace(",","."))
#                     product.price_market = float(str(col[8]).strip().replace(",","."))
#                     product.package_quantity = int(str(col[9]).strip())
#                     product.package_weight = float(str(col[10]).strip().replace(",","."))
#                     product.palette_quantity = int(str(col[11]).strip())
#                     product.palette_weight = float(str(col[12]).strip().replace(",","."))
#                     product.barcode = str(col[13]).strip()

#                     palette_count = 0
#                     if len(str(col[14]).strip()) > 0 and str(col[14]).strip() != "***":
#                         palette_count = int(float(str(col[14]).strip()))
#                     product.total_production = palette_count * product.package_quantity * product.palette_quantity
#                     quantity = palette_count * product.palette_quantity * product.package_quantity
#                     # if not str(col[15]).strip().startswith("***"):
#                     #     quantity = int(str(col[15]).strip())
#                     #     price_production = int(str(col[16]).strip())
#                     product.save()
                    
#                     if quantity > 0:
                    
#                         product_id = product.id
                        
#                         percentage = quantity/product.total_production
#                         production = Production()
#                         production.product_id = product_id
#                         production.user_id = request.user.id
#                         production.quantity = quantity
#                         production.created_at = date_str
#                         production.status_id = 4
#                         production.note_store = "Manuel Girilen Kayıt"
#                         production.note_filling = "Manuel Girilen Kayıt"
#                         production.production_quantity = quantity
#                         production.save()
#                         material_list = ProductMaterial.objects.filter(is_active=True, product_id=product_id).values('material_id','material__name', 
#                         'material__measurement_type_id','quantity').prefetch_related('material_product_material')
                      
#                         for mat in material_list:
                        
#                             stock_list = Stock.objects.filter(is_active=True, material_id=mat['material_id']).order_by('created_at')
#                             stock_id = 3 # select * from material_stock order by id
#                             if stock_list:
#                                 stock_id = stock_list[0].id
#                             p_m = ProductionMaterial()
#                             p_m.production_id=production.id
#                             p_m.stock_id = stock_id
#                             p_m.quantity = float(mat['quantity'])*percentage
#                             p_m.save()

#                         material_list = ProductionMaterial.objects.filter(production_id=production.id).values('quantity','stock__price', 'stock__price_future', 
#                                 'stock__money_rate_price')
#                         total_price = 0.0
#                         total_price_future = 0.0
#                         for mat in material_list:
#                             total_price += mat['quantity'] *  mat['stock__price'] * mat['stock__money_rate_price']
#                             total_price_future += mat['quantity'] *  mat['stock__price_future'] * mat['stock__money_rate_price'] 
                        
#                         p_s = ProductStock()
#                         p_s.production_id = production.id
#                         p_s.product_id = production.product.id
#                         p_s.quantity = quantity
#                         p_s.price = round(total_price,2)
#                         p_s.price_future = round(total_price_future,2)
#                         p_s.created_at = date_str
#                         p_s.save()       
                
#             except Exception as ex:
#                 print(f'{i} could not find product_id:{str_1} ex:{str(ex)} ')
#                 print()

#     context = {
#         'userprofile': userprofile,
        
#     }
#     return render(request, 'companies/save_product_manuel.html', context)
   



# @login_required(login_url = 'login')
# def save_materials_manual(request):
#     """Malzemeleri ve stok bilgilerini excel dosyasından kayıt etme 
#     http://127.0.0.1:8000/companies/save_materials_manual/"""
#     userprofile = UserProfile.objects.get(user=request.user)  
#     if request.user.is_admin == False:
#        context = { 'userprofile': userprofile,  }
#        return render(request, '403.html', context) 
#     company_owner = request.user.userprofile.company_id
#     company_list = Company.objects.all().exclude(id=company_owner)
#     date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     material_list = []
   
#     try:
#         MaterialEntry.objects.all().delete()
#         ProductionMaterial.objects.all().delete()
#         Stock.objects.all().delete()
        
#         Shipment.objects.all().delete()
#        # ProductMaterial.objects.all().delete()
        
#         ProductStock.objects.all().delete()
#         Stock.objects.all().delete()
#      ##   Material.objects.all().delete()
#     except Exception as ex:
#         print(str(ex))


#     if "POST" == request.method:
    
#         excel_file = request.FILES["excel"]
#         df = pd.DataFrame(excel_file)

#         sheet_index= 0
#         df = pd.read_excel(io=excel_file, sheet_name=sheet_index, usecols=range(0,15), skiprows=1)
#         df = df.where(df.notna(), "***")
#         print(df.head())
#         print(df) 
#         material_counter = 0
#         despatch_counter = 1
#         for i, col in enumerate(df.itertuples(), 1):
#             print(i, col)
#             if material_counter == 0: 
#                 ship = Shipment()
#                 ship.company_id = 2 #cosmer
#                 # ship.company_logistic = request.POST["company_logistic"]
#                 ship.despatch_number = "ilk_giris_" + str(despatch_counter)
#                 ship.note = "manuel girilen kayıtlar"
#                 ship.created_at = date_str
#                 ship.user_id = request.user.id
#                 ship.status_id = 5
               

#                 ship.save()
#             stock = Stock()
#             ma = MaterialEntry()
#             try:
#                 code = str(col[1]).strip() 
#                 try:
#                     material = Material.objects.get(code=code)
#                 except :
#                     material = Material()
#                     material.code = code
                
#                 material.name = str(col[2]).strip()
#                 material.description = str(col[3]).strip()

#                 material_type = str(col[4]).strip()
#                 mat_type = MaterialType.objects.get(name=material_type)
#                 material.type_id = mat_type.id

#                 usage_type_name = str(col[5]).strip()
#                 try:
#                     usage_type = UsageType.objects.get(name=usage_type_name)
#                 except:
#                     usage_type = UsageType(name=usage_type_name,material_type_id=mat_type.id,is_active=True)
#                     usage_type.save()
                
#                 material.usage_type_id = usage_type.id

#                 measure_type_name = str(col[6]).strip()
#                 measurment_type = MeasurementType.objects.get(name=measure_type_name)
#                 material.measurement_type_id = measurment_type.id

#                 # alert_limit = str(col[10]).strip()
#                 # if not alert_limit.startswith("**"):
#                 #     material.alert_limit = int(alert_limit) 
                
#                 material.save()
#                 if i == 21:
#                     print()
#                 stock.material_id = material.id
#                 stock.quantity = float(str(col[7]).strip().replace(",","."))
#                 price_str = str(col[8]).strip().replace(",",".")
#                 money_id = 1
#                 price_try = 1
#                 price = 0
#                 if stock.quantity != 0 and price_str != "***":
#                     if "EUR" in price_str:
#                         money_id = 4
#                         price_try = 20.09
#                     if "USD" in price_str:
#                         money_id = 2
#                         price_try = 18.96

#                     price = float(price_str[0: price_str.index(" ")])
#                 stock.price = price
#                 stock.shipment_id = ship.id
#                 stock.created_at = date_str
#                 stock.price_try = price_try
#                 if stock.price_future == 1:
#                     stock.price_future = stock.price * 1.25
#                 stock.save()
#                 ma = MaterialEntry()
#                 ma.material_id = material.id
#                 ma.shipment_id = ship.id
#                 ma.quantity = stock.quantity
#                 ma.note = "Mauel Giriş"
#                 ma.created_at = date_str
#                 ma.is_active = True
#                 ma.save()

#                 material_counter += 1
#                 if material_counter == 15:
#                     material_counter = 0
#                     despatch_counter += 1
#             except Exception as ex:
#                 print(f'{i} error:{str(ex)}')
                

#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#     }
#     return render(request, 'companies/update_company.html', context)
   



# @login_required(login_url = 'login')
# def create_product_materials(request):
#     # today = datetime.today()
#     userprofile = UserProfile.objects.get(user=request.user)  
#     if request.user.is_admin == False:
#        context = { 'userprofile': userprofile,  }
#        return render(request, '403.html', context) 
#     company_owner = request.user.userprofile.company_id
#     company_list = Company.objects.all().exclude(id=company_owner)
#     date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     material = Material.objects.filter(id =132).values('id','name')
#     product_list = Product.objects.filter(is_active=True).order_by("name").values('id',"name","meter","package_quantity","package_weight",
#     "palette_quantity","palette_weight","total_production","vat","price","price_market","barcode","limit","description","type__name")
#     material_list = []
#     material_list.append(material)
    
#     row_num = 0
#     workbook = xlsxwriter.Workbook('borline.xlsx')
#     worksheet = workbook.add_worksheet()
#     bold = workbook.add_format({'bold': True})
#     for product in product_list:
#         material_list = ProductMaterial.objects.filter(product_id = product['id']).order_by("material__name").values('material__id',"material__name","quantity","cost_type__name")
#         if len(material_list) == 0:
#             material_list = []
#             material_list.append(material)

        


#         col_num = 0 
#         for key, value in product.items():
#             worksheet.set_row(row_num, None, bold)
#             worksheet.write(row_num, col_num, key)
#             worksheet.write(row_num+1, col_num, value)
            
#             col_num += 1
            
#         row_num += 2
#         key_added = False
        
#         for material in material_list:
#             col_num = 0
#             for key, value in material.items():
#                 if key_added == False:
#                     worksheet.set_row(row_num, None, bold)
#                     worksheet.write(row_num, col_num, key)
#                     worksheet.write(row_num+1, col_num, value)
                    
#                 else:
#                     worksheet.write(row_num, col_num, value)
                    
#                 col_num += 1
#             if not key_added:
#                 key_added = True
#                 row_num += 2
#             else:
#                 row_num += 1
#         row_num += 2


#     workbook.close()
   
#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#     }
#     return render(request, 'companies/update_company.html', context)
   




# @login_required(login_url = 'login')
# def save_product_materials(request):
#     # today = datetime.today()
#     userprofile = UserProfile.objects.get(user=request.user)  
#     if request.user.is_admin == False:
#        context = { 'userprofile': userprofile,  }
#        return render(request, '403.html', context) 
#     company_owner = request.user.userprofile.company_id
#     company_list = Company.objects.all().exclude(id=company_owner)
#     date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     material_list = []
   
#     if "POST" == request.method:
    
#         excel_file = request.FILES["excel"]
#         df = pd.DataFrame(excel_file)

#         sheet_index= 0
#         df = pd.read_excel(io=excel_file, sheet_name=sheet_index, usecols=range(0,5))
#         df = df.where(df.notna(), "***")
#         print(df.head())
#         print(df) 
#         material_counter = 0
#         despatch_counter = 1
#         for i, col in enumerate(df.itertuples(), 1):
#             print(i, col)
#             try:
#                 str_1 = str(col[1]) 
#                 if str_1.startswith('ÜRÜN KODU'):
#                     product_id = int(str_1.replace('ÜRÜN KODU : ','').strip())
#                     product = Product.objects.get(id = product_id)
#                     total_production = float(str(col[4]).replace("ADET/TIR",""))
#                     product.total_production = total_production
#                     product.save()
#                     ProductMaterial.objects.filter(product_id = product_id).delete()

#                 if not str_1.startswith('ÜRÜN KODU') and not str_1.startswith('malzeme') and not str_1.startswith('***'):
#                     material_id = int(col[1])
#                     quantity = float(str(col[4]).replace(",","."))
#                     cost_type = 2
#                     if str(col[5]).startswith("İÇ"):
#                         cost_type = 1
                    
#                     mat = ProductMaterial()
#                     mat.product_id = product_id
#                     mat.material_id = material_id
#                     mat.is_active = True
#                     mat.quantity = quantity
#                     mat.cost_type_id = cost_type
#                     mat.save()

                
#             except:
#                 print(f'{i} could not find')
#                 pass

#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#     }
#     return render(request, 'companies/save_product_materials.html', context)



    

# @login_required(login_url = 'login')
# def save_product_material_new(request):
#     # today = datetime.today()
#     userprofile = UserProfile.objects.get(user=request.user)  
#     if request.user.is_admin == False:
#        context = { 'userprofile': userprofile,  }
#        return render(request, '403.html', context) 
#     company_owner = request.user.userprofile.company_id
#     company_list = Company.objects.all().exclude(id=company_owner)
#     date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     material_list = []
   
#     if "POST" == request.method:
    
#         excel_file = request.FILES["excel"]
#         df = pd.DataFrame(excel_file)

#         sheet_index= 0
#         df = pd.read_excel(io=excel_file, sheet_name=sheet_index, usecols=range(0,15))
#         df = df.where(df.notna(), "***")
#         print(df.head())
#         print(df) 
#         material_counter = 0
#         despatch_counter = 1
#         for i, col in enumerate(df.itertuples(), 1):
#             print(i, col)
#             try:
#                 str_1 = str(col[1]).strip() 
#                 if not str_1.startswith('***')  and not str_1.startswith('id') and str(col[10]) != "***":
                  
#                     product_id = int(str_1)
#                     product = Product.objects.get(id = product_id)
#                     product.name = str(col[2]).strip()
#                     product.meter = int(str(col[3]).strip())
#                     product.package_quantity = int(str(col[4]).strip())
#                     product.package_weight = float(str(col[5]).strip().replace(",","."))
#                     product.palette_quantity = int(str(col[6]).strip())
#                     product.palette_weight = float(str(col[7]).strip().replace(",","."))
#                     product.total_production = float(str(col[8]).strip().replace(",","."))
#                     product.vat = float(str(col[9]).strip().replace(",","."))
#                     product.price = float(str(col[10]).strip().replace(",","."))
#                     product.price_market = float(str(col[11]).strip().replace(",","."))
#                     product.barcode = (str(col[12]).strip())
#                     product.limit = int(str(col[13]).strip())
#                     product.description = (str(col[14]).strip())
#                     type_name = str(col[15]).strip()
#                     product_type_id = ProductType.objects.get(name=type_name)
#                     product.type_id = product_type_id
#                     product.save()
                  
#                     ProductMaterial.objects.filter(product_id = product_id).delete()

#                 elif not str_1.startswith('***')  and not str_1.startswith('id') and not str_1.startswith('material'):
#                     material_id = int(col[1])
#                     quantity = float(str(col[3]).replace(",","."))
#                     cost_type = 2
#                     if str(col[4]).startswith("İÇ"):
#                         cost_type = 1
                    
#                     mat = ProductMaterial()
#                     mat.product_id = product_id
#                     mat.material_id = material_id
#                     mat.is_active = True
#                     mat.quantity = quantity
#                     mat.cost_type_id = cost_type
#                     mat.save()

                
#             except:
#                 print(f'{i} could not find')
#                 pass

#     context = {
#         'userprofile': userprofile,
#         'company_list': company_list,
#     }
#     return render(request, 'companies/save_product_material_new.html', context)
   
