from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', 
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            next_page=reverse_lazy('restaurants:restaurant_list')
        ), 
        name='login'
    ),

    path('logout/', 
        auth_views.LogoutView.as_view(
            next_page=reverse_lazy('home')
        ), 
        name='logout'
    ),
    
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('home/', views.home, name='home'),

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ), 
         name='password_reset'),

    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),

    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html'
         ), 
         name='password_change'),

    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ), 
         name='password_change_done'),
]
