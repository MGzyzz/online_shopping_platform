from django.urls import reverse
from django.test import TestCase, Client

from accounts.models import User

from .models import Shop, Product
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile


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
                                    {'name': 'New name', 'description': 'Test new description',
                                     'logo': 'def.png', 'theme': 'white'})

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


class ShopDeleteCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='myemail@gmail.com', phone='77014779047', password='123')
        self.shop = Shop.objects.create(user_id=self.user.id, name='New', description='Test description', theme='black')

    def test_delete_success(self) -> None:
        self.client.login(username='myemail@gmail.com', password='123')

        response = self.client.post(reverse('shop_delete', kwargs={"id": self.shop.id}))

        with self.assertRaises(ObjectDoesNotExist):
            Shop.objects.get(id=self.shop.id)
        self.assertFalse(Shop.objects.filter(id=self.shop.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', kwargs={'id': self.user.id}))

    def test_delete_false(self) -> None:
        self.client.login(username='myemail@gmail.com', password='123')

        response = self.client.post(reverse('shop_delete', kwargs={'id': self.shop.id+1}))

        self.assertTrue(Shop.objects.filter(id=self.shop.id))
        self.assertEqual(response.status_code, 404)


class ShopListCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='myemail@gmail.com', phone='77014779047', password='123')
        self.shop = Shop.objects.create(user_id=self.user.id, name='New', description='Test description', theme='black')

    def test_success(self) -> None:
        client = Client()

        url = reverse('shop_view', kwargs={'shop_id': self.shop.id})

        response = client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertIn('shop', response.context)
        self.assertIn('products', response.context)
        self.assertIn('category_product', response.context)
        self.assertEqual(response.context['shop'], self.shop)

    def test_false(self) -> None:
        client = Client()

        url = reverse('shop_view', kwargs={'shop_id': self.shop.id + 1})

        response = client.get(url)

        self.assertEqual(response.status_code, 404)


class ProfileCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='myemail@gmail.com', phone='77014779047', password='123')
        self.other_user = User.objects.create_user(email='bad@mail.ru', phone='77011919099', password='555')
        self.url = reverse('profile', kwargs={'id': self.user.id})

    def test_profile_success(self) -> None:
        self.client.login(username='myemail@gmail.com', password='123')

        response = self.client.get(self.url)

        self.assertIn('shops', response.context)
        self.assertEqual(response.status_code, 200)

    def test_fail_profile(self) -> None:
        self.client.login(username='bad@mail.ru', password='555')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)


# class ProductCreateCase(TestCase):
#     def setUp(self) -> None:
#         self.user = User.objects.create_user(email='pr@gmail.com', password='123', phone='87014779047')
#         self.shop = Shop.objects.create(user_id=self.user.id, name='New', description='Test description', theme='black')
#
#     def test_product_create_success(self) -> None:
#         self.client.login(username='pr@gmail.com', password='123')
#         image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
#         response = self.client.post(reverse('create_product', kwargs={"shop_id": self.shop.id}), {
#             'shop': self.shop.id,
#             'name': 'test product',
#             'description': 'test test',
#             'vendor_code': "111111",
#             'quantity': 1111,
#             'price': 10000,
#             'image': [image_file]
#
#         }, follow=True)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(Product.objects.filter(name='test product'))
