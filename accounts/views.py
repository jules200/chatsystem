from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import *

# Create your views here.
def loginview(request):
    if request.user.is_authenticated:
        return redirect('feeds')
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user_login = authenticate(email=email, password=password)

        if user_login:
            login(request, user_login)
            return redirect('main')
        else:
            return HttpResponse("Failled")
    return render(request, 'accounts/login.html')

def logoutview(request):
    logout(request)
    return redirect('login')
    # return redirect('login')
    
def new_account(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname= request.POST['lname']
        email= request.POST['email']
        phone= request.POST['phone']
        photo= request.FILES['photo']
        password= request.POST['password']

        userexit = MyUser.objects.filter(email=email).exists()
        if userexit:
            return HttpResponse("Exit")
        else:

            obj=MyUser.objects.create_user(phone=phone, first_name=fname, last_name=lname, email=email, profile_image=photo,  password=password)
            obj.save()
            if obj:
                user_login = authenticate(email=email, password=password)
                if user_login:
                    login(request, user_login)
                    return redirect('main')
            

    return render(request, 'accounts/register.html')

# def home(request):
#     return render(request, 'profile.html')

def editprofile(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname= request.POST['lname']
        email= request.POST['email']
        photo= request.FILES['photo']

        update = MyUser.objects.filter(pk = request.user.id).first()
        update.first_name=fname
        update.last_name=lname
        update.email=email
        update.profile_image=photo
        update.update()

        if update:
            return redirect('home')
        else:
            return HttpResponse("Failled")
def deleteuser(request, user_id):
    userdelete = MyUser.objects.get(pk=user_id)
    if userdelete.delete():                                                                                   
        messages.success(request, "User deleted Successfull")
    else:
        messages.success(request, "Deletion Failled") 
    
    return redirect('users')

@login_required
@permission_required('account.view_myuser', raise_exception=True)
def uuser(request):
    user_obj=MyUser.objects.all
    return render(request, 'users.html',{'user_obj':user_obj})