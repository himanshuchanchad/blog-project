from django.shortcuts import render
from .forms import signup,userdata,blogcreate,add_comment
from .models import userdetail,blog_post,comments
from django.http import  HttpResponseRedirect,HttpResponse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import  User
from .models import userdetail
# Create your views here.
def home(request):
    return render(request,"home.html")
@login_required
def index(request):
    return render(request,"index.html")

def register(request):
    if request.method=='POST':
        user=signup(data=request.POST)
        detail=userdata(data=request.POST)
        if user.is_valid() and detail.is_valid():

            newuser=user.save()
            newuser.set_password(newuser.password)
            newuser.save()
            profile=detail.save(commit=False)
            profile.user=newuser
            if 'img' in request.FILES:
                profile.img=request.FILES['img']
            profile.about=detail.cleaned_data['about']
            profile.save()
            return HttpResponseRedirect(reverse(home))
        else:
            print("NOT VALID")
    else:
        user = signup()
        detail = userdata()
    context={
        'form':user,
        'detail':detail
    }
    return render(request,"register.html", context)

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if username and password :
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return HttpResponseRedirect(reverse(index))
            else:
                return HttpResponse("user doesn't exists or password doesn't match!")
        else:
            return HttpResponse("Enter the password !")
    else:
        return render(request,"login.html")

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse(home))

@login_required
def changepass(request):
    if request.method=='POST':
            user=User.objects.get(username=request.user)
            oldpass=request.POST.get('password')
            newpass=request.POST.get('newpassword')
            cnpass=request.POST.get('cnpassword')
            print(user.check_password(oldpass))
            if not user.check_password(oldpass):
                return HttpResponse("INCORRECT OLD PASSWORD")
            else:
                if newpass!=cnpass:
                    return HttpResponse("PASSWORD DOESNT MATCH")
                else:
                    user.set_password(newpass)
                    user.save()
                    return HttpResponse("PASSWORD SUCCESSFULLY CHANGED")
    else:
        return render(request,"changepass.html")
@login_required
def detail(request):
    userinfo=User.objects.get(username=request.user)
    qs = userdetail.objects.get(user=request.user)
    print(qs.img)
    context = {
        'info':userinfo,
        'qs': qs
    }
    return render(request,"detail.html",context)