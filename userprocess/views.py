 

import email
from itertools import count, product
from wsgiref.util import shift_path_info

import django
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta

from account.models import Account, UserAuth, UserProfile, UserRight
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.core import serializers
from django.db.models import F, Sum,Max
from django.db.models.functions import Cast,TruncMonth
from django.db.models import TextField
import requests
from forex_python.converter import CurrencyRates
from django.db.models import Q, Count


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.forms.models import model_to_dict
from datetime import date
from django.conf import settings
import datetime



from account.models import Account, UserProfile, UserAuth  
from common.models import Logs

@login_required(login_url = 'login')
def users(request):
    
    userprofile = UserProfile.objects.get(user=request.user)   
    try:
        user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="userprocess")
    except UserAuth.DoesNotExist:
        context = {
        'userprofile': userprofile,
        }
        return render(request, '403.html',context)
    
 


    user_list = Account.objects.filter(is_active=True).order_by('email').values('id','email','first_name','last_name',)
    #right_list = UserRight.objects.values('id','description')
    context = {
        'userprofile': userprofile,
        'user_list': user_list,
    }
    return render(request, 'userprocess/processes.html', context)
 

@login_required(login_url = 'login')
def edit_password(request,id):
  
    userprofile = UserProfile.objects.get(user=request.user)   
    try:
        user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="userprocess")
    except UserAuth.DoesNotExist:
        context = {
        'userprofile': userprofile,
        }
        return render(request, '403.html',context)
    
    try:
        user = Account.objects.get(id=id)
    except Account.DoesNotExist:
        context = {
        'userprofile': userprofile,
        }
        return render(request, '403.html',context)

    if "POST" in request.method:
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, f' {user.email} için Şifre Güncellendi! ')
            return redirect('users')
        else:
            messages.success(request, f' {user.email} için Şifreler Aynı Değil! ')
    
  
    context = {
        'userprofile': userprofile,
        'user': user,
    }
    return render(request, 'userprocess/edit.html', context)


@login_required(login_url = 'login')
def edit_rights(request,id):
  
    userprofile = UserProfile.objects.get(user=request.user)   
    try:
        user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="userprocess")
    except UserAuth.DoesNotExist:
        context = {
        'userprofile': userprofile,
        }
        return render(request, '403.html',context)
    
    try:
        user = Account.objects.get(id=id)
    except Account.DoesNotExist:
        context = {
        'userprofile': userprofile,
        }
        return render(request, '403.html',context)
    right_list = UserRight.objects.all().values('id','description').order_by('description')
    user_right_list = list(UserAuth.objects.filter(user_id=id).values_list('right_id', flat=True))
    if "POST" in request.method:
        UserAuth.objects.filter(user_id=id).delete()
        for key,value in request.POST.items():
          #  print (key,value)
            if str(key).startswith('r__'):
                right = UserAuth(user=user,right_id=int(value)).save()
        messages.success(request, f' {user.email} için Yetkiler Güncellendi! ')
        return redirect('users')

    for r in right_list:
        if r['id'] in user_right_list:
            r['checked'] = 1
    context = {
        'userprofile': userprofile,
        'user': user,
        'right_list': right_list,
    }
    return render(request, 'userprocess/rights.html', context)


@login_required(login_url = 'login')
def new_user(request):
   
    userprofile = UserProfile.objects.get(user=request.user)   
    try:
        user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="userprocess")
    except UserAuth.DoesNotExist:
        context = {
        'userprofile': userprofile,
        }
        return render(request, '403.html',context)
    
    
    
    if 'POST' in request.method:
        email = request.POST['email']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

       


        if new_password == confirm_password:
            new_user = Account()
            new_user.email = email
            new_user.username = email
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.set_password(new_password)
            new_user.is_active = True
            new_user.save()
            new_profile = UserProfile()
            new_profile.user = new_user
            new_profile.phone_number = phone_number
            new_profile.save()
            messages.success(request, new_user.email + ' Yeni Kullanıcı EKlendi.')
            return redirect('edit_rights/'+str(new_user.id))
        else:
            messages.error(request, 'Şifreler aynı değil!')
            return redirect('new_user')
   
    context = {
        'userprofile': userprofile,
    }
    return render(request, 'userprocess/new_user.html', context)
 

     
