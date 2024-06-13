"""
Tests for ingredients API.
"""
from decimal import Decimal


from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Ingredient,
    Recipe,
    )

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

def create_user(email='test@example.com', password='Pass123'):
    """"Creates and return an user."""
    return get_user_model().objects.create_user(email=email, password=password)

def detail_url(ingredient_id):
    """Create and return a detail url """
    return reverse('recipe:ingredient-detail', args=[ingredient_id])

class PublicIngredientsApiTests(TestCase):
    """Test for public requests of the ingredients API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required to access ingredients list"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTests(TestCase):
    """Test for logged in requests of the ingredients API."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_ingredients_list(self):
        """Test retrieving list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Lenguado')
        Ingredient.objects.create(user=self.user, name='sal')

        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)


        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user"""
        other_user = create_user(email='jose@example.com', password='test1234')
        Ingredient.objects.create(user=other_user, name='Weed')
        ingredient = Ingredient.objects.create(user=self.user, name='Avocado')
        
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating an ingredient for a given user."""
        ingredient = Ingredient.objects.create(user=self.user, name='Salmon')

        payload = {'name': 'Orange'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredient for a given user."""
        ingredient = Ingredient.objects.create(user=self.user, name='jabalí')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
        """Test listing ingredients by those assigned to recipes."""
        in1 = Ingredient.objects.create(user=self.user, name='Apples')
        in2 = Ingredient.objects.create(user=self.user, name='Tomatoes')
        r1 = Recipe.objects.create(user=self.user, 
                                   title='a tasty helado',
                                   price=Decimal('3.5'),
                                   time_minutes=10,
                                   )
        r1.ingredients.add(in1)

        res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})
        s1= IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_ingredient_unique(self):
        """Test filtered ingredients return an unique list."""
        ing = Ingredient.objects.create(user=self.user, name='Eggs')
        Ingredient.objects.create(user=self.user, name='Lentejas')

        recipe1 = Recipe.objects.create(
            user=self.user,
            title='Egg Benedict',
            price=Decimal(10.0),
            time_minutes=60,
            )
        recipe2 = Recipe.objects.create(
            user=self.user,
            title='Herb Eggs',
            price=Decimal('13.2'),
            time_minutes=12,
        )

        recipe1.ingredients.add(ing)
        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)











    









