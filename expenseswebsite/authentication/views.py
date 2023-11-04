from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator


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
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {'fieldValues': request.POST}

        if not User.objects.filter(username=username).exists():
            if len(password) < 6:
                messages.error(request, "Password is too short")
                return render(request, 'authentication/register.html', context)

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)


            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})

            activate_url = 'http://'+domain+link
            email_subject = "Activate your account"
            email_body = 'Hi ' + user.username + ' Use this link to activate your account:\n' + activate_url

            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@semycolon.com', 
                [email],
            )
            email.send(fail_silently=False)

            messages.success(request, "Account created Successfully")
            return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=str(urlsafe_base64_decode(uidb64))
            user=user.objects.get(pk=id)

            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+' User already activated')


            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()
            messages.success(request,"User activated successfully")
            return redirect('login')
        except Exception as ex:
            pass
        return redirect('login')
    


class loginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')
    
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']

        if username and password :
            user=auth.authenticate(request,username=username,password=password)

            if user is not None:

                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome '+user.username+' You are now logged in')
                    return redirect('expenses')
        
                messages.error(request,"Account is not activated,please check  your email")
                return render(request,'authentication/login.html')
        
            messages.error(request,'Invalid credentials,try again')
            return render(request,'authentication/login.html')
        
        messages.error(request,'Please fill in all fields')
        return render(request,'authentication/login.html')
    
class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')





