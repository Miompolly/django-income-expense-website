from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
# Create your views here.



class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Email is in use,shoose other one'},status=409)
        
        return JsonResponse({'email_valid':True})

class UsernameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username error should only contains alpnumeric characters'},status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username is in use,shoose other one'},status=409)
        
        return JsonResponse({'username_valid':True})


class RegistationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    
    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        context={
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(username=username).exists():

                if len(password)<6:
                    messages.error(request,"Password is too short")
                    return render(request,'authentication/register.html',context)
                
                user=User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.save()
                messages.success(request,"Account created Successfully")
                return render(request,'authentication/register.html')
        

      
        return render(request,'authentication/register.html')


