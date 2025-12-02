from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from restaurants.test_restaurants.mixins import AuthMixin  # Using your factory-based mixin
from django.contrib.auth import get_user_model

User = get_user_model()


class TestLoginView(AuthMixin, TestCase):

    def test_login_page_should_load_successfully(self):
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_user_should_login_with_correct_credentials(self):
        self.create_user(username="testuser")  # create user via factory
        url = reverse("login")
        response = self.client.post(url, {"username": "testuser", "password": "pass123"})
        self.assertRedirects(response, reverse("home"))


class TestLogoutView(AuthMixin, TestCase):

    def test_user_should_logout_successfully(self):
        self.login_user()
        url = reverse("logout")
        response = self.client.post(url)
        self.assertRedirects(response, reverse("home"))


class TestSignUpView(AuthMixin, TestCase):

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
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertRedirects(response, reverse("login"))


class TestPasswordResetView(AuthMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.user = self.create_user()

    def test_password_reset_page_should_load(self):
        url = reverse("password_reset")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_email_should_be_sent(self):
        url = reverse("password_reset")
        response = self.client.post(url, {"email": self.user.email})
        self.assertEqual(response.status_code, 302)


class TestPasswordResetDoneView(AuthMixin, TestCase):

    def test_password_reset_done_page_should_load(self):
        url = reverse("password_reset_done")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPasswordResetConfirmView(AuthMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.user = self.create_user()

    def test_password_reset_confirm_page_should_load_with_valid_uid_and_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})

        self.login_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class TestPasswordResetCompleteView(AuthMixin, TestCase):

    def test_password_reset_complete_page_should_load(self):
        url = reverse("password_reset_complete")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPasswordChangeView(AuthMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.login_user(self.user)

    def test_password_change_page_requires_login(self):
        self.client.logout()
        url = reverse("password_change")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_access_password_change_page(self):
        url = reverse("password_change")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_change_password(self):
        url = reverse("password_change")
        response = self.client.post(url, {
            "old_password": "pass123",
            "new_password1": "newpass12345",
            "new_password2": "newpass12345"
        })
        self.assertRedirects(response, reverse("password_change_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass12345"))


class TestPasswordChangeDoneView(AuthMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.login_user(self.user)

    def test_password_change_done_page_should_load(self):
        url = reverse("password_change_done")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
