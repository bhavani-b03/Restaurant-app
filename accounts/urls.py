from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # Password change
    path('password/change/', 
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
        name='password_change'
    ),
    path('password/change/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name='password_change_done'
    ),

    # Password reset
    path('password/reset/', 
        views.CustomPasswordResetView.as_view(
            template_name="registration/password_reset_form.html",       # form user sees
            email_template_name="registration/password_reset_email.html", # HTML email
            subject_template_name="registration/password_reset_subject.txt"
        ),
        name='password_reset'
    ),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('home/', views.home, name='home'),
]
