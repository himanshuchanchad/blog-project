from django import forms
from .models import (
    comments, userdetail, blog_post
)
from django.contrib.auth.models import User

class signup(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    pass2=forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        all_clean_data=super().clean()
        password=all_clean_data['password']
        pass2=all_clean_data['pass2']
        if password!=pass2:
            raise forms.ValidationError(" PASSWORD DOESN'T MATCH TRY AGAIN !   ")
    class Meta():
        model=User
        fields=('first_name','last_name','username','password')


class userdata(forms.ModelForm):
    img=forms.ImageField(required=False)
    about=forms.CharField(widget=forms.Textarea(),required=False)
    class Meta():
        model = userdetail
        fields = ['img','about']


class blogcreate(forms.ModelForm):
    class Meta():
        model = blog_post
        fields = '__all__'


class add_comment(forms.ModelForm):
    class Meta():
        model = comments
        fields = '__all__'