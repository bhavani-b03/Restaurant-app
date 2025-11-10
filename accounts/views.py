from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after signup
            return redirect('home')  # Redirect to homepage after signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


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
