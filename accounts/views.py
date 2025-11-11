from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

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



from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.template.loader import render_to_string

class CustomPasswordResetView(PasswordResetView):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        # Render subject
        subject = render_to_string(subject_template_name, context).strip()

        # Render HTML message
        html_message = render_to_string(email_template_name, context)

        # Send email with html_message (forces HTML MIME)
        send_mail(
            subject=subject,
            message='Fallback plain text',  # required fallback
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message      # THIS is what marks it as HTML
        )
