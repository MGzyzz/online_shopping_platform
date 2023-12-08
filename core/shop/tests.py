from django.urls import reverse
from django.test import TestCase

from accounts.models import User

from .models import Shop


class ShopCreateCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='myemail@gmail.com', phone='77014779047', password='123')

    def test_shop_creation(self) -> None:
        self.client.login(username='myemail@gmail.com', password='123')

        response = self.client.post(reverse('shop_create'), {
            'name': 'New',
            'description': 'Test description',
            'theme': 'black'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Shop.objects.count(), 1)
        self.assertRedirects(response, reverse('profile', kwargs={'id': self.user.id}))
        new_shop = Shop.objects.first()
        self.assertEqual(new_shop.user, self.user)

    def test_shop_created_invalid(self) -> None:
        self.client.login(username='myemail@gmail.com', password='123')
        response = self.client.post(reverse('shop_create'), {
            'name': 'New',
            'description': 'Test description',
            'theme': 'greeen'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice. greeen is not one of the available choices.')


class ShopUpdateCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='myemail@gmail.com', phone='77014779047', password='123')
        self.shop = Shop.objects.create(user_id=self.user.id, name='New', description='Test description', theme='black')

    def test_update_success(self) -> None:
        self.client.login(username='myemail@gmail.com', password='123')
        response = self.client.post(reverse('shop_update', kwargs={'id': self.shop.id}),
                                    {'name': 'New name', 'description': 'Test new description', 'logo': 'def.png', 'theme': 'white'})

        updated_shop = Shop.objects.get(id=self.shop.id)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', kwargs={'id': self.user.id}))
        self.assertEqual(updated_shop.name, 'New name')
        self.assertEqual(updated_shop.description, 'Test new description')

    def test_bad_update(self) -> None:
        self.client.login(username='myemail@gmail.com', password='123')

        response = self.client.post(reverse('shop_update', kwargs={'id': self.shop.id}),
                                    {'name': 'NEW NAME', 'description': 'Test new description', 'logo': 'def.png',
                                     'theme': 'green'})

        self.assertContains(response, 'Select a valid choice. green is not one of the available choices.')
        self.assertEqual(response.status_code, 200)



