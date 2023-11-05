from django.shortcuts import redirect, render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# def index(request):
#     user = request.user
#     exists = UserPreference.objects.filter(user=user).exists()

#     if exists:
#         user_preferences = UserPreference.objects.get(user=user)
#     else:
#         user_preferences = UserPreference(user=user, currency='')

#     if request.method == 'GET':
#         currency_data = load_currency_data()
#         request.session['currency_data'] = currency_data

#         return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences })

#     elif request.method == 'POST':
#         currency = request.POST['currency']

#         if exists:
#             user_preferences.currency = currency
#             user_preferences.save()
#         else:
#             new_user_preferences = UserPreference(user=user, currency=currency)
#             new_user_preferences.save()
#         messages.success(request, "Changes Saved")
#         return HttpResponseRedirect(reverse('preferences'))

# def load_currency_data():
#     file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

#     with open(file_path, 'r') as json_file:
#         data = json.load(json_file)

#     currency_data = [{'name': k, 'value': v} for k, v in data.items()]
#     return currency_data



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
        currency = request.POST.get('currency')  # Use 'get' to safely retrieve the selected value

        if currency != 'Choose...':  # Check if the selected value is not "Choose..."
            if exists:
                user_preferences = UserPreference.objects.get(user=user)
                user_preferences.currency = currency
                user_preferences.save()
            else:
                UserPreference.objects.create(user=user, currency=currency)
                messages.success(request, "Changes Saved")

    return redirect('preferences')