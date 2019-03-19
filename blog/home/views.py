from django.shortcuts import render,get_object_or_404,redirect
from .forms import signup,userdata,blogcreate,add_comment
from .models import userdetail,blog_post,comments
from django.http import  HttpResponseRedirect,HttpResponse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import  User
# Create your views here.
def home(request):
    qs=blog_post.objects.all()
    context={
        'blog':qs
    }
    return render(request,"home.html",context)

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
                return HttpResponseRedirect(reverse(home))
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
def profile_update(request):
    if request.method=='POST':
        user=userdetail.objects.get(user=request.user)
        profile=userdata(data=request.POST)
        if profile.is_valid():
            if 'img' in request.FILES:
                user.img=request.FILES['img']
                user.save(update_fields=['img'])
            elif user.about!=profile.cleaned_data['about']:
                user.about=profile.cleaned_data['about']
                user.save(update_fields=['about'])
        return HttpResponseRedirect(reverse(detail))
    else:
        profile=userdata()
    context={
        'profileupdate':profile,
    }
    return render(request,'profile_update.html',context)


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

@login_required
def createblog(request):
    if request.method=='POST':
        title=request.POST['Title']
        content=request.POST['content']
        blog=blog_post.objects.create(user=request.user,title=title,blog_content=content)
        blog.save()
        return HttpResponseRedirect(reverse(dispblog))
    else:
        return render(request,"addblog.html")

def dispblog(request):
    blog=blog_post.objects.filter(user=request.user)

    context={
        'blog':blog,
    }
    return render(request,"generalbloglist.html" ,context)

def detailblog(request,title):
    qs=get_object_or_404(blog_post,slug=title)
    getcomment=comments.objects.filter(blog=qs)
    if request.method=='POST':
        commentadd=request.POST['comment']
        if qs.user==request.user:
            c = comments.objects.create(user=request.user, blog=qs, comment=commentadd,approved=True)
            c.save()
        else:
            c=comments.objects.create(user=request.user,blog=qs,comment=commentadd)
            c.save()
    else:
        pass
    context={
        'displaycomment':getcomment,
        'b':qs,
    }
    return render(request,"blogdetail.html",context)

def comment_approve(request,pk):
    comment=get_object_or_404(comments,pk=pk)
    print(comment)
    slug=comment.blog.slug
    comment.approval()
    return redirect('blogdetail',title=slug)



