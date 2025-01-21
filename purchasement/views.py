
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Account
from common.models import Money
from purchasement.models import PurchasementItem, PurchasementStepDetail, PurchasementDetail, PurchasementType
from django.db.models import F, Value, Func


class PurchasementListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, project_id, *args, **kwargs):
        # `project_id` kwargs'dan geliyor
        purchasment_step_details = PurchasementStepDetail.objects.filter(project_id=project_id).values(
            "id", "name", "no", "description", "made_in", "supplier",
            "producer_brand", "customs_required", "pa", "pm", "pd", "notes",
            "currency", "purchasement_step", "purchasement_type", "purchasement_step__purchasement_type_id", "project_id"
        ).order_by('no')
        user_list = Account.objects.filter(is_active=True).annotate(
            name=Func(
                F('first_name'),
                Value(' '),
                F('last_name'),
                function='CONCAT'
            )
        ).values('id', 'email', 'name', 'user_type')
    
        purchasement_type_list = PurchasementType.objects.filter(is_active=True).values("id", "code")
        print(purchasment_step_details[0])
        response_data = {
            "purchasment_step_details": list(purchasment_step_details),
            "user_list": list(user_list),
            "purchasement_type_list": list(purchasement_type_list),
        }

        return Response(response_data, status=status.HTTP_200_OK)


     

class PurchasementDetailView(APIView):
   # permission_classes = (IsAuthenticated,)

    def put(self, request):

        body_data = request.data

        # Body verisini işle
        # for key, value in body_data.items():
        #     print(f"{key}: {value}")

        # Verileri body_data'dan al
        project_id = int(body_data.get('projectId', 0))
        project_type_id = int(body_data.get('projectTypeId', 0))
        purchasement_type_id = int(body_data.get('purchasementTypeId', 0))
        purchasement_step_detail_id = int(body_data.get('purchasementStepDetailId', 0))
  
        purchasement_details = []
        try:
            purchasement_details = PurchasementDetail.objects.filter(
                project_id=project_id, purchasement_step_detail_id=purchasement_step_detail_id).values(
                "id", "name", "assigned_users", "owner_id", "title",
                "duration", "start_date", "finish_date", "status", 
                "notes", "no", "progress", 
                "progress_comments", "complete_date", "md_approval_status"
            ).order_by('no')

       
            if not purchasement_details:
                purchasement_items = PurchasementItem.objects.filter(purchasement_type_id=purchasement_type_id, project_type_id=project_type_id).values("id", "name", "no")

                for item in purchasement_items:
                    # PurchasementDetail oluştur
                    PurchasementDetail.objects.create(
                        project_id=project_id,
                        purchasement_type_id=purchasement_type_id,
                        purchasement_step_detail_id=purchasement_step_detail_id,
                        purchasement_item_id=item["id"],  # Item ID'sini alıyoruz
                        name=item["name"],  # Item ID'sini alıyoruz
                        #purchasement_detail.assigned_users.add(request.user)

                        owner_id=request.user.id,  # Owner kullanıcıyı istersen buradan set edebilirsin
                        duration=None,  # Duration bilgisi girilmediği için null bırakıldı
                        start_date=None,  # Başlangıç tarihi yok
                        finish_date=None,  # Bitiş tarihi yok
                        status="Pending",  # Default bir status veriyoruz
                        notes=None,  # Notlar eklenmediği için null bırakıldı
                        no=item["no"],  # Sıra numarası default 1
                        progress=0.00,  # Başlangıçta progress 0
                        progress_comments=None,  # Progress comment yok
                        complete_date=None,  # Tamamlama tarihi yok
                        md_approval_status="Not Started"  # Varsayılan onay durumu
                    )
                    print(f"Created PurchasementDetail for item: {item}")


                            # Var olan PurchasementDetail verilerini çek
                purchasement_details = PurchasementDetail.objects.filter(
                    project_id=project_id,
                    purchasement_step_detail_id=purchasement_step_detail_id
                ).values(
                    "id", "name", "assigned_users", "owner_id", "title",
                    "duration", "start_date", "finish_date", "status",
                    "notes", "no", "progress",
                    "progress_comments", "complete_date", "md_approval_status"
                ).order_by('no')

        except Exception as e:
            print(e)
            #for purch_type in purchasement_type_id:

            




        user_list = Account.objects.filter(is_active=True).annotate(
            name=Func(
                F('first_name'),
                Value(' '),
                F('last_name'),
                function='CONCAT'
            )
        ).values('id', 'email', 'name', 'user_type')
       # print(cost_items_list[0])
        response_data = {
            "user_list": list(user_list),
            "purchasement_details": list(purchasement_details),
        }

        return Response(response_data, status=status.HTTP_200_OK)

class PurchasementStepDetailUpdateView(APIView):
    def put(self, request):
        body_data = request.data  # Gelen veri, list şeklinde olmalı
        print(body_data)
        if not isinstance(body_data, list):
            return Response({"error": "Invalid data format. Expected a list."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Güncelleme işlemi için döngü başlat
            for data in body_data:
                obj_id = data.get("id")
                if not obj_id:
                    continue  # ID yoksa atla
                
                # Güncellenmesi gereken objeyi getir
                try:
                    obj = PurchasementStepDetail.objects.get(id=obj_id)
                except PurchasementStepDetail.DoesNotExist:
                    print(f"Object with ID {obj_id} does not exist.")
                    continue  # ID bulunamazsa atla
                
                # Objeyi güncelle
                obj.made_in = data.get("made_in", obj.made_in)
                obj.supplier = data.get("supplier", obj.supplier)
                obj.producer_brand = data.get("producer_brand", obj.producer_brand)
                obj.customs_required = data.get("customs_required", "?") 
                obj.pa_id = data.get("pa", obj.pa_id)
                obj.pm_id = data.get("pm", obj.pm_id)
                obj.pd_id = data.get("pd", obj.pd_id)
                obj.notes = data.get("notes", obj.notes)

                # Güncellemeleri kaydet
                obj.save()
                print(f"Updated object: {obj}")

            return Response({"message": "Purchasement details updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": f"An error occurred during the update process: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PurchasementTemplateUpdateView(APIView):
    def put(self, request):
        data = request.data  # Gelen veri, list şeklinde olmalı
        print(data['project_id'])
        purchasement_step_list = data['purchasement_steps']

     
        try:
            # 1. Eski kayıtları sil
            project_id = data['project_id']
            PurchasementDetail.objects.filter(project_id=project_id).delete()
            PurchasementStepDetail.objects.filter(project_id=project_id).delete()

            creater_id = request.user.id

            # 2. Yeni kayıtları ekle
            for data in purchasement_step_list:
                print(data)
                PurchasementStepDetail.objects.create(
                project_id=project_id,
                purchasement_step=step,
                name=data['name'],
                no=data['no'],
                purchasement_type_id=data['purchasement_type_id'],
                description=f"...",
                made_in="...",
                supplier="...",
                producer_brand="...",
                customs_required='?',
                pa_id=creater_id,
                pm_id=creater_id,
                pd_id=creater_id,
                notes=f"...",
                currency=Money.objects.first()  # Varsayılan bir para birimi
            )
 

            return Response({"message": "Purchasement details updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": f"An error occurred during the update process: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class PurchasementDetailUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        """
        Birden fazla PurchasementDetail objesini günceller.
        Beklenen veri formatı:
        [
          {
            "id": 1,
            "duration": "2 weeks",
            "start_date": "2023-01-01",
            "finish_date": "2023-01-15",
            "title": "New Title",
            "assigned_users": [2, 3],      # ManyToMany güncellemek için user ID listesi
            "progress": "50",
            "progress_comments": "Task is half done",
            "status": "In Progress",
            "complete_date": "2023-01-30",
            "notes": "Updated notes"
          },
          {
            "id": 2,
            "duration": "3 weeks",
            ...
          }
        ]
        """
        body_data = request.data

        # Gelen verinin list olup olmadığını kontrol et
        if not isinstance(body_data, list):
            return Response(
                {"error": "Invalid data format. Expected a list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            for data in body_data:
                obj_id = data.get("id")
                if not obj_id:
                    # ID yoksa atla
                    continue

                # Objeyi getir
                obj = PurchasementDetail.get(id=obj_id)
                print(data)
                # Güncellenecek alanlar
                obj.duration = data.get("duration", obj.duration)
                obj.title = data.get("title", obj.title)
                obj.progress = data.get("progress", obj.progress)
                obj.progress_comments = data.get("progress_comments", obj.progress_comments)
                obj.status = data.get("status", obj.status)
                obj.notes = data.get("notes", obj.notes)

                # Tarih alanları için '' kontrolü yap
                start_date = data.get("start_date", obj.start_date)
                obj.start_date = None if start_date == '' else start_date

                finish_date = data.get("finish_date", obj.finish_date)
                obj.finish_date = None if finish_date == '' else finish_date

                complete_date = data.get("complete_date", obj.complete_date)
                obj.complete_date = None if complete_date == '' else complete_date

                # ManyToMany: assigned_users (liste şeklinde user id'leri bekliyoruz)
                if "assigned_users" in data:
                    user_ids = data["assigned_users"] or []
                    # İlgili user objelerini çekip set ediyoruz
                    obj.assigned_users.add(*user_ids)
                obj.save()
                print(f"Updated PurchasementDetail object: {obj}")

            return Response(
                {"message": "Purchasement details updated successfully."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"Error: {e}")

            return Response(
                {"error": f"An error occurred during the update process: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
