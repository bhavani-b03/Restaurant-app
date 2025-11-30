from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from tests.mixins import UserMixin

class TestLoginView(UserMixin, TestCase):

    def test_login_page_should_load_successfully(self):
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_user_should_login_with_correct_credentials(self):
        url = reverse("login")
        response = self.client.post(url, {"username": "testuser", "password": "pass123"})
        self.assertRedirects(response, reverse("home"))


class TestLogoutView(UserMixin, TestCase):

    def test_user_should_logout_successfully(self):
        self.login()
        url = reverse("logout")
        response = self.client.post(url)
        self.assertRedirects(response, reverse("home"))


class TestSignUpView(UserMixin, TestCase):

    def test_signup_page_should_load(self):
        url = reverse("signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_should_register_successfully(self):
        url = reverse("signup")
        response = self.client.post(url, {
            "username": "newuser",
            "password1": "complexpass123",
            "password2": "complexpass123"
        })
        self.assertEqual(User.objects.filter(username="newuser").exists(), True)
        self.assertRedirects(response, reverse("login"))


class TestPasswordResetView(UserMixin, TestCase):

    def test_password_reset_page_should_load(self):
        url = reverse("password_reset")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_email_should_be_sent(self):
        url = reverse("password_reset")
        response = self.client.post(url, {"email": self.user.email})
        self.assertEqual(response.status_code, 302)

class TestPasswordResetDoneView(UserMixin, TestCase):

    def test_password_reset_done_page_should_load(self):
        url = reverse("password_reset_done")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPasswordResetConfirmView(UserMixin, TestCase):

    def test_password_reset_confirm_page_should_load_with_valid_uid_and_token(self):

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPasswordResetCompleteView(UserMixin, TestCase):

    def test_password_reset_complete_page_should_load(self):
        url = reverse("password_reset_complete")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPasswordChangeView(UserMixin, TestCase):

    def test_password_change_page_requires_login(self):
        url = reverse("password_change")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_logged_in_user_can_access_password_change_page(self):
        self.login()
        url = reverse("password_change")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_change_password(self):
        self.login()
        url = reverse("password_change")
        response = self.client.post(url, {
            "old_password": "pass123",
            "new_password1": "newpass12345",
            "new_password2": "newpass12345"
        })
        self.assertRedirects(response, reverse("password_change_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass12345"))


class TestPasswordChangeDoneView(UserMixin, TestCase):

    def test_password_change_done_page_should_load(self):
        self.login()  # User must be logged in to access this page
        url = reverse("password_change_done")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
