from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text

from .forms import RegistrationForm
from .token import account_activation_token

# Create your views here.
def account_register(request):
    # This is the registration page
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        user = registerForm.save(commit=False)
        user.email = registerForm.cleaned_data['email']
        user.set_password(registerForm.cleaned_data['password'])
        # After email verification will make user as active 
        user.is_active = False
        user.save()
        # Setup email
        current_site = get_current_site(request)
        subject = 'Activate your account'
        message = render_to_string('account/registration/account_activation_email.html',{
            'user': user,
            'doamin': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject=subject, message=message)
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/registration.html', {'form': registerForm})


