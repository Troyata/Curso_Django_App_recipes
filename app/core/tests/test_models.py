"""

Test for models

"""
from decimal import Decimal

from django.test import TestCase  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore

from core import models


class ModelTests(TestCase):
    """ Tests models """

    def test_create_user_with_email_successful(self):
        """ Test creating an user with email successful """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    
    def test_new_user_email_normalized(self):
        """ Test email is normalized """
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        ''' Test if email field is missing and raises error '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'Sample123')

    def test_create_superuser(self):
        ''' Test creating a superuser '''
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'sample123'
        )
        self.assertTrue(user.is_superuser)  #Esto te lo da el permissionMixin
        self.assertTrue(user.is_staff)

    
    def test_create_recipe(self):
        """Test create recipes is succesful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Recipe Name',
            time_minutes=5,
            price=Decimal('5.5'),
            description='Sample recipe description',
        )

        self.assertEqual(str(recipe),recipe.title)
