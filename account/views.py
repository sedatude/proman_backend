from urllib.request import Request
from django.db.models import query
from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, UserProfile
 
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from .forms import UserForm, UserProfileForm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import status
from rest_framework.response import Response

import requests

  
class UserDetailsView(APIView):
   
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        id = request.user.id
        profilen_path = UserProfile.objects.filter(user_id=id).values('profile_picture').first()['profile_picture'] 
        user_info = Account.objects.filter(id=id).values('id', 'first_name', 'last_name', 'email', 'user_type')[0]
        user_info['profile_picture'] = profilen_path
 
        response_data = {
            "user_info": user_info,  # Convert QuerySet to list
        }

        return Response(response_data, status=status.HTTP_200_OK)


def login(request): 
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('users')
        else:
            messages.error(request, 'Lütfen bilgileri tekrar kontrol ediniz!')
            return redirect('login')
    return render(request, 'accounts/login.html')

 
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
  #  messages.success(request, 'Çıkış Yapıldı.')
    return redirect('login')




@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Şifre Güncellendi.')
                return redirect('change_password')
            else:
                messages.error(request, 'Lütfen Geçerli Şifreyi giriniz!')
                return redirect('change_password')
        else:
            messages.error(request, 'Şifreler aynı değil!')
            return redirect('change_password')
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
         
        'userprofile': userprofile,
    }
    return render(request, 'accounts/change_password.html',context)



@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    try:
        if 'POST' in request.method:
            # for key,value in request.POST.items():
            #     print (f'userprofile.{key} = request.POST[\'{key}\']')
            u_user = Account.objects.get(id = request.user.id)
            u_user.first_name = request.POST['first_name']
            u_user.last_name = request.POST['last_name']
            userprofile.phone_number = request.POST['phone_number']
            userprofile.address_line_1 = request.POST['address_line_1']
            # userprofile.city = request.POST['city']
            # userprofile.country = request.POST['country']
            if "profile_picture" in request.FILES:
                userprofile.profile_picture = request.FILES["profile_picture"]
            userprofile.save()
            u_user.save()
            messages.success(request, 'Profil Güncellendi.')
            return redirect('edit_profile')
     
    except Exception as ex:
        print(str(ex))
    context = {
        
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


