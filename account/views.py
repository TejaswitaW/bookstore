from django.shortcuts import render
from django.shortcuts import redirect

from forms import RegistrationForm

# Create your views here.
def account_register(request):
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
