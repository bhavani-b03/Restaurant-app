from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', 
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            next_page=reverse_lazy('home')
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
]
