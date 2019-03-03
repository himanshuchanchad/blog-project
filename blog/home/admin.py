from django.contrib import admin
from .models import userdetail, comments, blog_post

# Register your models here.
admin.site.register(userdetail)
admin.site.register(comments)
admin.site.register(blog_post)
#admin.site.register()