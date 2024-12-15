from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

 

from account.models import UserAuth, UserProfile
import os, pandas as pd
from django.contrib import messages, auth
from django.db.models.functions import Cast, Coalesce, TruncDate
from django.db.models import Count, TextField, F, Sum,Max,Q
from django.db.models import FloatField, TextField


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer

class ProjectCreateView(APIView):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectUpdateView(APIView):
    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDeleteView(APIView):
    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        project.delete()
        return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# @login_required(login_url = 'login')
# def dashboard(request):
#     userprofile = UserProfile.objects.get(user=request.user)   
#     # if request.user.is_staff == False:
#     #     context = { 'userprofile': userprofile,  }
#     #     return render(request, '403.html', context)
    
#     product_list = Product.objects.all().filter(is_active=True).order_by("name")
#     # material_count = Material
#     material_lower = []
#     material_empty = []
#     # material_lower = Material.objects.filter(is_active=True).order_by('name').values('name','id','alert_limit').prefetch_related('material_stock').annotate(total=Coalesce(Sum('material_stock__quantity'),0)
#     #         ).filter(total__lte=F('alert_limit')).exclude(total=0).count()
#     # material_empty = Material.objects.filter(is_active=True).order_by('name').values('name','id','alert_limit').prefetch_related('material_stock').annotate(total=Coalesce(Sum('material_stock__quantity'),0)
#     #         ).filter(total=0).count()

#     product_stock = int(ProductStock.objects.filter(status_id=1).aggregate(total=Coalesce(Sum('quantity'),0))['total'])
#     production_stock = int(ProductionStock.objects.filter(status_id__in=[2,3,6]).aggregate(total=Coalesce(Sum('quantity'),0))['total'])

    
#     date_end = datetime.date.today()
#     date_start = (datetime.date.today()- datetime.timedelta(days=300))
    

    
#     # data_list = ProductionStock.objects.order_by('created_at__date') .filter().values('created_at__date'
#     # ).annotate(total=Sum('quantity'))
#     # for data in data_list:
#     #     data['total'] = int(data['total'])
#     #     data['created_at__date'] = data['created_at__date'].strftime("%Y-%m-%d")

#     data_list = ProductionStock.objects.order_by('created_at__date').values(
#     'product_id', 'product__name'
#     ).annotate(
#         total=Sum('production_quantity', output_field=FloatField())
#     ).annotate(
#         read_date=Cast(TruncDate('created_at'), output_field=TextField())
#     ).filter(
#         read_date__range=[date_start, date_end]
#     )

#     print(data_list)
#     context = {
#         'userprofile': userprofile,
#         'product_list': product_list,
#         'material_lower': material_lower,
#         'material_empty': material_empty,
#         'product_stock': product_stock,
#         'production_stock': production_stock,
#         'data_json' : json.dumps(list(data_list)),
#     }
#     return render(request, 'main.html', context)

    
# @login_required(login_url = 'login')
# def product_dashboard(request):
#     userprofile = UserProfile.objects.get(user=request.user)   
#     # if request.user.is_staff == False:
#     #     context = { 'userprofile': userprofile,  }
#     #     return render(request, '403.html', context)
    
#     product_list = Product.objects.all().filter(is_active=True).order_by("name")
    
#     context = {
#         'userprofile': userprofile,
#         'product_list': product_list,
#     }
#     return render(request, 'products/product.html', context)

# @login_required(login_url = 'login')
# def test(request):
#     userprofile = UserProfile.objects.get(user=request.user)   
  
    
#     context = {
#         'userprofile': userprofile,
#     }
#     return render(request, 'test.html', context)



# @login_required(login_url = 'login')
# def product_processes(request):
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="product_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)
#     userprofile = UserProfile.objects.get(user=request.user)   
   
    
#     product_list = Product.objects.all().filter(is_active=True).order_by("name")
    
#     context = {
#         'userprofile': userprofile,
#         'product_list': product_list,
#     }
#     return render(request, 'products/processes.html', context)



# @login_required(login_url = 'login')
# def product_materials(request,id):
#     userprofile = UserProfile.objects.get(user=request.user)  

#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="product_material_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)
     
#     try:
#         product = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

#     material_list = []
#     total_product = 1
#     material_list = ProductMaterial.objects.filter(product_id =id).values('product__name','quantity','material__name','quantity','material__cost_type__name').order_by('material__cost_type__name','product__name')
#     for mat in material_list:
#         if "KAPAK" in str(mat['material__name']):
#             total_product = mat['quantity']
#             break

#     context = {
#         'userprofile': userprofile,
#         'material_list': material_list,
#         'total_product': total_product,
#         'product': product,
        
#     }
#     return render(request, 'products/product_materials.html', context)
    
        
        


# @login_required(login_url = 'login')
# def product_materials_total(request):

#     # pl = Product.objects.filter(is_active=True)
#     # for  p in pl:
#     #     pw = ProductMaterial.objects.filter(product_id=p.id)
#     #     if len(pw) == 0:
#     #         product_material = ProductMaterial()
#     #         product_material.product_id = p.id
#     #         product_material.material_id = 133
#     #         product_material.quantity = 1
#     #         product_material.save()



#     userprofile = UserProfile.objects.get(user=request.user)   
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="product_material_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

  
#     #product_list = ProductMaterial.objects.filter(is_active=True).values('product_id','product__name','product__meter').annotate(total=Count('material'))
#     product_list = Product.objects.filter(is_active=True).values('id','name','meter','internal_weight').prefetch_related('product_material').annotate(total=Coalesce(Count('product_material'),0))
#     #{'id': 124, 'name': 'Bulaşık Deterjanı Elmalı 650', 'meter': 650, 'total': 14, 'kilo': 3.14828}
#     #product_list = Product.objects.filter(is_active=True).values('id','name','meter').prefetch_related('product_material').annotate(total=Coalesce(Count('product_material'),0)).annotate(kilo=Coalesce(Sum('product_material__quantity'),0))
    
#     # for product in product_list:
#     #     kilo = ProductMaterial.objects.filter(product_id=product['id']).values('id','material__name').aggregate(total=Coalesce(Sum('quantity'),0))
#     #     name = product['name']
#     #     print(f'isim:{name} kilo:{kilo}')

    
#     context = {
#         'userprofile': userprofile,
#         'product_list': product_list,
        
       
#     }
#     return render(request, 'products/product_materials_total.html', context)



# @login_required(login_url = 'login')
# def product_material_new(request):
#     userprofile = UserProfile.objects.get(user=request.user)   
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="product_material_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)
#     material_range = range(1,26)
#     if "POST" in request.method:
#         # for key,value in request.POST.items():
#         #     print (f'product_material.{key} = request.POST[\'{key}\']')
#         product = Product.objects.get(id =int(request.POST['product']) )

#         counter = 0
#         for index in material_range:
#             mat_index = "material_"+str(index)
#             material_id = int(request.POST[str(mat_index)])
#             if material_id > 0:
#                 counter += 1
#                 product_material = ProductMaterial()
#                 product_material.product_id = product.id
#                 product_material.material_id = material_id
#                 product_material.quantity = float(request.POST["quantity_"+ str(index)].replace(",","."))
#                 product_material.save()

#         Logs(site="product_material_new", text=str(product.name)+ " adlı ürün için malzemeler eklendi.", type="Ürün için Yeni Malzeme Liste Kaydı."
#             , created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), record_id=product.id, user_info=request.user.first_name+" "+request.user.last_name).save() 

#         messages.success(request, f'{product.name} adlı  Ürün için Malzeme Listesi Eklendi.')
         
#         return redirect('product_materials')
   
#     material_list = Material.objects.filter(is_active=True)
#     product_list = Product.objects.filter(is_active=True)
    
    
#     context = {
#         'userprofile': userprofile,
#         'material_list': material_list,
#         'product_list': product_list,
#         'material_range': material_range,
#         # 'usage_type_list_json':  json.dumps(list(usage_type_list)),
#     }
#     return render(request, 'products/material_new.html', context)



# @login_required(login_url = 'login')
# def product_material_edit(request,id):
#     """ reçete güncelleme işlemi yapılıyor. 
#     Suyu en son iç maliyetlerin toplamından çıkararak otomatik olarak hesaplıyoruz."""
#     userprofile = UserProfile.objects.get(user=request.user)   
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="product_material_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

#     try:
#         product = Product.objects.get(id=id)
#     except Exception as ex:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)
       
#     material_list = Material.objects.filter(is_active=True).values('id','name','cost_type__name').order_by('name')
#     if "POST" in request.method:
#         # for key,value in request.POST.items():
#         #     print (f'product_material.{key} = request.POST[\'{key}\']')
#         product = Product.objects.get(id=id)
#         ProductMaterial.objects.filter(product_id=id).delete()
#         internal_weight = 0 
#         counter = 0
#         material_water_id = Material.objects.values('id').get(name="SAF SU")['id']
#         for index in range(1,26):   
#             mat_index = "material_"+str(index)
#             material_id = int(request.POST[str(mat_index)])
           
#             if material_id > 0:
#                 product_material = ProductMaterial()
#                 product_material.product_id = product.id
#                 product_material.material_id = material_id
#                 product_material.quantity = float(request.POST["quantity_"+ str(index)].replace(",","."))
#                 for mat in material_list:
#                     if mat['id'] == material_id and mat['cost_type__name'] == "İÇ MALİYET" and material_id != material_water_id:
#                         internal_weight += product_material.quantity
#                 if material_id != material_water_id:
#                     counter += 1
#                     product_material.save()
#         product.internal_weight = round(internal_weight, 4)

#         product_material = ProductMaterial()
#         product_material.product_id = product.id
#         product_material.material_id = material_water_id
#         product_material.quantity = round(product.meter/1000.0 - internal_weight, 4)
#         product_material.save()
#         counter += 1
#         product.material_count = counter
#         product.save()
#         Logs(site="product_material_edit", text=str(product.name)+ " adlı ürün için malzemeler güncellendi.", type="Ürün için  Malzeme Listesi Güncellendi."
#             , created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), record_id=product.id, user_info=request.user.first_name+" "+request.user.last_name).save() 

#         messages.success(request, f'{product.name} adlı  Ürün için Malzeme Listesi Güncellendi.')
         
#         return redirect('/../../product_materials/'+str(id))
   
    
#     #print(material_list[0])
#     product_material_list = ProductMaterial.objects.filter(product_id=id).values('id','material_id','quantity').order_by('material__cost_type__name')
#     material_range = range(1,len(product_material_list))
#     new_list_range = 0 
#     if len(product_material_list) < 26:
#         new_list_range = range(len(product_material_list)+1,26)
    
    
#     context = {
#         'userprofile': userprofile,
#         'material_list': material_list,
#         'product': product,
#         'product_material_list': product_material_list,
#         'material_range': material_range,
#         'new_list_range': new_list_range,
#         # 'usage_type_list_json':  json.dumps(list(usage_type_list)),
#     }
#     return render(request, 'products/material_edit.html', context)

# @login_required(login_url = 'login')
# def new_product(request):
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="product_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

#     userprofile = UserProfile.objects.get(user=request.user)   

#     if "POST" in request.method:
#         # for key,value in request.POST.items():
#         #     print (f'product.{key} = request.POST[\'{key}\']')
#             product = Product()
#             product.type_id = request.POST['type_id']
#             product.name = request.POST['name']
#             product.description = request.POST['description']
#             product.barcode = request.POST['barcode']
#             product.meter = str(request.POST['meter']).replace(",",".")
#             #product.density = str(request.POST['density']).replace(",",".")
#             product.package_quantity = int(str(request.POST['package_quantity']).replace(",","."))
#             product.package_weight = str(request.POST['package_weight']).replace(",",".")
#             product.palette_quantity = int(str(request.POST['palette_quantity']).replace(",","."))
#             product.palette_weight = str(request.POST['palette_weight']).replace(",",".")
#             product.palette_package_quantity = product.palette_quantity / product.package_quantity
#             product.internal_weight = str(request.POST['internal_weight'])
#             product.external_weight = str(request.POST['external_weight'])
#             product.vat = str(request.POST['vat']).replace(",",".")
#             product.price = str(request.POST['price']).replace(",",".")
            
#             product.price_market = str(request.POST['price_market']).replace(",",".")
#             product.limit = str(request.POST['limit']).replace(",",".")
#             date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             product.updated_at = date_str
#             product.save()
#             ProductHistory(product_id = product.id, price=product.price, price_market=product.price_market, vat=product.vat, updated_at=date_str).save()


#             Logs(site="new_product", text=str(product.name)+ " adlı Ürün eklendi.", type="Yeni Ürün Kaydı."
#                 , created_at=date_str, record_id=product.id, user_info=request.user.first_name+" "+request.user.last_name).save() 
#             messages.success(request, f'{product.name} Adlı  Ürün Eklendi!')
#             return redirect('product_processes')
	    
#     product_list = Product.objects.all().filter(is_active=True)
#     type_list = ProductType.objects.filter(is_active=True).values('id','name')
    
#     context = {
#         'userprofile': userprofile,
#         'product_list': product_list,
#         'type_list': type_list,
#     }
#     return render(request, 'products/new.html', context)


# @login_required(login_url = 'login')
# def product_material_delete(request):
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="material_processes")
#     except UserAuth.DoesNotExist:
#         userprofile = UserProfile.objects.get(user=request.user)
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)
    
#     url = request.META.get('HTTP_REFERER')
#     id = int(request.POST['object_id'])
#     if "GET" != request.method:
#         try:
#             product = Product.objects.get(id=id)
#         except Exception as ex:
#             context = {
#         'userprofile': userprofile,
#         }
#             return render(request, '403.html',context)
#         ProductMaterial.objects.filter(product_id=product.id).exclude(material_id=133).delete()
        
#         messages.success(request, f'{product.name} adlı Ürünün Malzemeleri Silindi.')
#         return redirect(url)

# @login_required(login_url = 'login')
# def edit_product(request, id):
#     userprofile = UserProfile.objects.get(user=request.user)  
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="product_processes")
#     except UserAuth.DoesNotExist:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

     
#     try:
#         product = Product.objects.get(id=id, is_active=True)
      
#     except Exception as ex:
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)

#     if "POST" in request.method:
       
#         date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         price = float(str(request.POST['price']).replace(",","."))
#         vat = float(str(request.POST['vat']).replace(",","."))
#         price_market = float(str(request.POST['price_market']).replace(",","."))
#         if product.price != price or product.vat != vat or product.price_market != price_market:
#             ProductHistory(product_id = product.id, price=price, price_market=price_market, vat=vat, updated_at=date_str).save()

#         product.type_id = request.POST['type_id']
#         product.name = request.POST['name']
#         product.description = request.POST['description']
#         product.barcode = request.POST['barcode']
#         product.meter = str(request.POST['meter']).replace(",",".")
#     # product.density = str(request.POST['density']).replace(",",".")
#         product.package_quantity = int(str(request.POST['package_quantity']).replace(",","."))
#         product.package_weight = str(request.POST['package_weight']).replace(",",".")
#         product.palette_quantity = int(str(request.POST['palette_quantity']).replace(",","."))
#         product.palette_weight = str(request.POST['palette_weight']).replace(",",".")
#         product.palette_package_quantity = product.palette_quantity / product.package_quantity
#         product.internal_weight = str(request.POST['internal_weight'])
#         product.external_weight = str(request.POST['external_weight'])
#         product.vat = vat
#         product.price = price
        
#         product.price_market = price_market
#         product.limit = str(request.POST['limit']).replace(",",".")
        
#         product.updated_at = date_str
#         product.save()
    

#         Logs(site="edit_product", text=str(product.name)+ " adlı Ürün güncellendi.", type="Ürün Güncelleme."
#             , created_at=date_str, record_id=product.id, user_info=request.user.first_name+" "+request.user.last_name).save() 
#         messages.success(request, f'{product.name} Adlı  Ürün Güncellendi.!')
#         return redirect('product_processes')
	    
#     type_list = ProductType.objects.filter(is_active=True).values('id','name')
    
#     context = {
#         'userprofile': userprofile,
#         'product': product,
#         'type_list': type_list,
#     }
#     return render(request, 'products/edit.html', context)
	    
        
 



# @login_required(login_url = 'login')
# def delete_product(request):
#     try:
#         user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="product_processes")
#     except UserAuth.DoesNotExist:
#         userprofile = UserProfile.objects.get(user=request.user)
#         context = {
#         'userprofile': userprofile,
#         }
#         return render(request, '403.html',context)
    
#     url = request.META.get('HTTP_REFERER')
#     id = int(request.POST['object_id'])
#     if "GET" != request.method:
#         try:
#             product = Product.objects.get(id=id)
#         except Exception as ex:
#             context = {
#         'userprofile': userprofile,
#         }
#             return render(request, '403.html',context)
#         product.is_active = False
#         product.save()
#         messages.success(request, f'{product.name} adlı Ürün Silindi.')
#         return redirect(url)






# @login_required(login_url = 'login')
# def product_stock(request):
#     today = datetime.datetime.now()
#     this_month = today - timedelta(days=60)
#     #print(this_month.strftime("%Y-%m-%d %H:%M:%S"))
#     userprofile = UserProfile.objects.get(user=request.user)
   
#     stock_list = []
     
#     filter_type = 0
#     if "POST" in request.method:

#         filter_type = int(request.POST['filter_type'])
#         if filter_type == 1:
#             stock_list = Product.objects.filter(is_active=True).values(
#                 'palette_package_quantity','package_quantity','palette_quantity','name','id','limit'
#                 ).prefetch_related('production_product'
#                 ).annotate(total=Coalesce(Sum('production_product__production_quantity'),0)).filter(total__lte=F('limit')).exclude(total=0)
#         elif filter_type == 2:
#             stock_list = Product.objects.filter(is_active=True).values(
#                 'palette_package_quantity','package_quantity','palette_quantity','name','id','limit'
#                 ).prefetch_related('production_product').annotate(total=Coalesce(Sum('production_product__production_quantity'),0)).filter(total=0)
  
#     if filter_type == 0:
#         stock_list = Product.objects.filter(is_active=True).values(
#             'palette_package_quantity','package_quantity','palette_quantity','name','id','limit'
#             ).prefetch_related('production_product').annotate(total=Coalesce(Sum('production_product__production_quantity'),0))
#     #print(stock_list[0])
#     for stock in stock_list:
#         stock['package_quantity_total'] = int(stock['total'] / stock['package_quantity'])
#         stock['palette_quantity_total'] = int(stock['total'] / stock['palette_quantity'])
#     context = {
#         'userprofile': userprofile,
#         'stock_list': stock_list,
#         'filter_type': filter_type,
#     }
#     return render(request, 'products/product_stock.html', context)