from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions

from .models import Snippet
from .serializers import UserSerializer, GroupSerializer, SnippetSerializer
from .permissions import IsOwnerOrReadOnly


class IndexView(TemplateView):
    template_name = "client/index.html"


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)
