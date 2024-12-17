from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from .token import account_activation_token
from .models import UserBase

@login_required
def dashboard(request):
    # If user is logged in then allow to access orders page
    # orders = user_orders(request)
    return render(request, 'account/user/dashboard.html')
    # return render(request, 'account/user/dashboard.html',{'section':'profile', 'orders':orders})

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
        # After we send an email , we want to redirect them to somewhere
        return HttpResponse("Registered successfully and activation sent")

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/registration.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    # Decode uidb64, token this activate the user account.
    try:
        # Trying to get the data.
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')





