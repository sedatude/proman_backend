 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
  
 
from django.contrib import messages, auth
from django.forms.models import model_to_dict
from datetime import date, datetime
from django.conf import settings
import datetime
import requests
from datetime import timedelta
import datetime
import locale






class Common:
    @login_required(login_url = 'login')
    def days(request):
        return ['Pazartesi','Salı','Çarşamba','Perşembe','Cuma']

    @login_required(login_url = 'login')
    def months(request):
        return ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']

    @login_required(login_url = 'login')
    def month_days(request,month_index):
        input_dt = datetime.datetime.today()
        if month_index is None or month_index != 0:
            input_dt = input_dt + timedelta(days=32)
        day_num = input_dt.strftime("%d")
        first_month_start = input_dt - timedelta(days=int(day_num) - 1)
        input_dt = input_dt.replace(day=1)
        input_dt = input_dt + timedelta(days=32)
        second_month_start = input_dt.replace(day=1)
        locale.setlocale(locale.LC_ALL, "tr_TR.utf8")

        next_month=[]
        delta = second_month_start - first_month_start  
        week_number = -1
        week_counter = 0
        d_week = {}
        for i in range(delta.days):
            day = first_month_start + timedelta(days=i)
            if day.weekday() in [0,1,2,3,4]:
                
                week_number_temp = day.isocalendar().week
                if week_number != week_number_temp:
                    if week_number != -1: #ilk giriş değil listeye ekle
                        next_month.append(d_week)
                        d_week = {}
                    week_counter += 1
                    d_week = {'week':{week_counter}}
                    """Hafta değişti eğer pazaresiden başlamıyorsa eksik günleri boş kayıt olarak ekle"""
                    day_count = day.weekday()
                    week_number = week_number_temp
                    index = 0
                    while day_count > 0:
                        d_dict = {'date':""}
                        d_week[index] = d_dict
                        
                        index += 1
                        day_count -= 1
                    
                d_dict = {'date':day.date().strftime("%Y.%m.%d")}
                d_week[day.weekday()] = d_dict
        next_month.append(d_week)
        return next_month