from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField,SerializerMethodField,EmailField,ValidationError
from home.models import blog_post
from django.contrib.auth.models import User

class postserializer(ModelSerializer):
    user=SerializerMethodField()
    class Meta:
        model=blog_post
        fields=[
            'user',
            'title',
            'blog_content'
        ]

    def get_user(self,obj):
        return obj.user.username

class createserial(ModelSerializer):
    class Meta:
        model=blog_post
        fields=[
            'title',
            'blog_content'
        ]

class userloginserializer(ModelSerializer):
    email1=EmailField(label='confirm email')
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'email1',
            'password'
        ]
        extra_kwargs={
            "password":{
                "write_only":True
            }
        }
    def validate_email1(self,value):
        data=self.get_initial()
        email=data.get("email")
        email1=data.get("email1")
        if email!=email1:
            raise ValidationError("Email does not match")
        return value
    def create(self, validated_data):
        user=validated_data['username']
        email=validated_data['email']
        password=validated_data['password']
        userobf=User(username=user,email=email)
        userobf.set_password(password)
        userobf.save()

        return validated_data
