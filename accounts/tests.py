from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestAuthViews(TestCase):

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


    def test_logout(self):
        user = User.objects.create_user(username='test', password='password123')
        self.client.login(username='test', password='password123')

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # redirect


    def test_signup(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

        # POST Signup
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())


    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_password_reset(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')


    def test_password_reset_done(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')


    def test_password_reset_confirm(self):
        # you need fake uid and token
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': 'test', 'token': '123'}))
        self.assertEqual(response.status_code, 200)  # page still loads
        self.assertTemplateUsed(response, 'accounts/password_reset_confirm.html')


    def test_password_reset_complete(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_complete.html')


    def test_password_change(self):
        user = User.objects.create_user(username='test', password='password123')
        self.client.login(username='test', password='password123')

        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_change.html')


    def test_password_change_done(self):
        user = User.objects.create_user(username='test', password='password123')
        self.client.login(username='test', password='password123')

        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_change_done.html')
