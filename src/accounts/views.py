from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import UserLogin, UserRegistration


def login_view(request):
    form = UserLogin(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request,user)
        _next = _next or '/'
        return redirect(_next)
    return render(request, 'accounts/login.html', {'form': form})

def logoute_view(request):
    logout(request)
    return redirect('/')



def user_registration_view(request):
    if request.method == 'POST':
        form1 = UserRegistration(request.POST)
        if form1.is_valid():
            new_user = form1.save(commit=False)
            new_user.set_password(form1.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})

        return render(request, 'accounts/register.html', {'form1': form1})

    else:
        form1 = UserRegistration()
        context= {'form1': form1}
        return render(request, 'accounts/register.html', context)
