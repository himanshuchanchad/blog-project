from django.shortcuts import render
from .forms import signup,userdata,blogcreate,add_comment
from .models import userdetail,blog_post,comments
from django.http import  HttpResponseRedirect,HttpResponse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def home(request):
    return render(request,"home.html")

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