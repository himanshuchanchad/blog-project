from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
# Create your models here.
class userdetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='profile_pics',blank=True)
    about=models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class blog_post(models.Model):
    user=models.ForeignKey(User,models.SET_NULL,null=True)
    title=models.CharField(max_length=256,unique=False)
    blog_content=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    slug=models.SlugField(null=True,blank=True)
    # published=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def pre_save_blog(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)

pre_save.connect(pre_save_blog,sender=blog_post)


class comments(models.Model):
    blog=models.ForeignKey(blog_post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,models.SET_NULL,null=True)
    comment=models.TextField()
    approved=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blog.title}"

    def approval(self):
        self.approved = True
        self.save()