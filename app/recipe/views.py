"""
Views for the recipe API.
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
   """ View for manage recipe APIs."""

   serializer_class = serializers.RecipeDetailSerializer  #Usamos este serializer como base pq incluye todos los campos.
   queryset = Recipe.objects.all()
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
     """Retrive recipes for an authenticated user."""
     return self.queryset.filter(user = self.request.user).order_by('-id')
   
   def get_serializer_class(self):
      """Get the appropriate serializer class for a given request."""
      if self.action == 'list':
         return serializers.RecipeSerializer
      return self.serializer_class
   def perform_create(self, serializer):
      """Create a new recipe."""
      serializer.save(user = self.request.user)


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
   """Manage Tags in the database"""
   serializer_class = serializers.TagSerializer
   queryset = Tag.objects.all()
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
      """filter and return the results to only get user's tag"""
      return self.queryset.filter(user=self.request.user).order_by('-name')