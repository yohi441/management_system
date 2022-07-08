from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from management_system.models import Client
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from management_system.forms import LoginForm





def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def login_view(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    
    if request.method == "POST":
        pass



    context= {
        'form': form,
    }

    return render(request, 'login.html', context)


@login_required(login_url='/')
def dashboard(request):
    clients = Client.objects.all()
    count = clients.count()
    context = {
        'clients': clients,
        'count': count
    }

    return render(request, 'index.html', context)