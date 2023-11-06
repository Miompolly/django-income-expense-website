from django.shortcuts import redirect, render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
    user = request.user
    exists = UserPreference.objects.filter(user=user).exists()
    user_preferences = None
    currency_data = []

    if exists:
        user_preferences = UserPreference.objects.get(user=user)

    if request.method == 'GET':
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})

        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
    else:
        currency = request.POST.get('currency')  
        if currency != 'Choose...': 
            if exists:
                user_preferences = UserPreference.objects.get(user=user)
                user_preferences.currency = currency
                user_preferences.save()
                messages.success(request, "Changes Saved")
            else:
                UserPreference.objects.create(user=user, currency=currency)
                messages.success(request, "Changes Saved")

    return redirect('preferences')