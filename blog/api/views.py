from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView
from home.models import blog_post
from .serializers import postserializer,createserial,userloginserializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from .permissions import isowner
from django.db.models import Q

from django.contrib.auth.models import User

from rest_framework.pagination import PageNumberPagination

class createblog(CreateAPIView):
    queryset = blog_post.objects.all()
    serializer_class = createserial
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class blogdetailview(ListAPIView):
    queryset = blog_post.objects.all()
    serializer_class = postserializer

    def get_queryset(self, *args, **kwargs):
        # query_list = super(blogdetailview, self).get_queryset( *args, **kwargs)
        qs = blog_post.objects.all()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(blog_content__icontains=query)
            ).distinct()
        return qs

class blogupdateview(UpdateAPIView):
    queryset = blog_post.objects.all()
    serializer_class = createserial
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated,isowner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class blogdeleteview(DestroyAPIView):
    queryset = blog_post.objects.all()
    serializer_class = postserializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated,isowner]

class retrieve(RetrieveAPIView):
    queryset = blog_post.objects.all()
    serializer_class = postserializer
    lookup_field = 'slug'

class createuser(CreateAPIView):
    serializer_class = userloginserializer
    queryset = User.objects.all()