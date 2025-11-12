from django.shortcuts import render
from django.contrib.auth import login
# Create your views here.
def home(request):
    return render(request, 'home.html')

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
