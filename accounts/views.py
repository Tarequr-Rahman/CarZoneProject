from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'invalid login creadintial')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('pages:home')
    return redirect('pages:home')

def register(request):
    if request.method=="POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password :
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username already exists')
                return redirect('accounts:register')

            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email already exists')
                    return redirect('accounts:register')
                else:
                    user=User.objects.create(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
                    auth.login(request, user)
                    messages.success(request, 'you are loged in!')
                    return redirect('accounts:dashboard')
                    user.save()
                    messages.success(request, 'you are registered succesfully!')
                    return redirect('accounts:login')
        else:
            messages.error(request, 'password do not match')
            return redirect('accounts:register')            
    else:
        return render(request, 'accounts/register.html')
@login_required(login_url='accounts:login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data={
        'inquiries':user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)