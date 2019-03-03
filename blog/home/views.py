from django.shortcuts import render
from .forms import signup,userdata,blogcreate,add_comment
from .models import userdetail,blog_post,comments
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
            return render(request,"home.html")
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