from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Tag
from django.db import IntegrityError

class TestModels(TestCase):

    def test_recipes_private_by_default(self):
        test_user = User.objects.create_user(username='user1', password='123')
        recipe = Recipe.objects.create(
            title='test_recipe',
            chef=test_user,
        )
        self.assertEqual(recipe.public_status, 0)
    

    def test_number_of_chefs_kisses_method(self):
        test_user = User.objects.create_user(username='user1', password='123')
        test_user2 = User.objects.create_user(username='user2', password='123')
        recipe = Recipe.objects.create(
            title='test_recipe',
            chef=test_user,
        )
        recipe.chefs_kisses.set([test_user, test_user2])
        self.assertEqual(recipe.number_of_chefs_kisses(), 2)


    def test_tag_color_must_be_unique(self):

        with self.assertRaises(IntegrityError) as context:
            tag1=Tag.objects.create(
                tag='tag1',
                color='#ffffff',
            )
            tag2=Tag.objects.create(
                tag='tag2',
                color='#ffffff',
            )

        self.assertTrue('UNIQUE constraint failed' in str(context.exception))

    def test_slugs_must_be_unique(self):

        with self.assertRaises(IntegrityError) as context:
            test_user = User.objects.create_user(username='user1', password='123')
            test_user2 = User.objects.create_user(username='user2', password='123')
            recipe1=Recipe.objects.create(
                title='title1',
                chef=test_user,
                slug='a-slug',
            )
            recipe2=Recipe.objects.create(
                title='title2',
                chef=test_user2,
                slug='a-slug',
            )
        self.assertTrue('UNIQUE constraint failed' in str(context.exception))

    def test_random_slug_function_generates_random_str(self):
        test_user = User.objects.create_user(username='user1', password='123')
        test_user2 = User.objects.create_user(username='user2', password='123')
        recipe1=Recipe.objects.create(
            title='title1',
            chef=test_user,
        )
        recipe2=Recipe.objects.create(
            title='title2',
            chef=test_user2,
        )
        self.assertFalse(recipe1.slug == recipe2.slug)
