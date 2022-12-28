from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.template.context_processors import csrf

from crispy_forms.utils import render_crispy_form
from django.urls import reverse, reverse_lazy

from accounts.forms import UserRegistrationForm, UserLoginForm

success_url = reverse_lazy('index')

# Create your views here.
def login_view(request):
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(success_url)

        return render(request, 'accounts/login.html', {'form': form})

    context = {'form': UserLoginForm(request)}
    return render(request, 'accounts/login.html', context)
        

def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    
    if request.method == 'POST':
        
        # inline validation using htmx
        if request.htmx:
            ctx = {}
            ctx.update(csrf(request))

            form_html = render_crispy_form(form, context=ctx)
            return HttpResponse(form_html)

        else:
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(success_url)

    return render(request, 'accounts/login.html', {'form': UserRegistrationForm()})

def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))


