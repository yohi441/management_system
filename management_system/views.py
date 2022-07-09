from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from management_system.models import Client, Item
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from management_system.forms import LoginForm, ClientForm, ItemForm





def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def login_view(request):
    
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('dashboard'))
    else:
        form = LoginForm(request)

    context= {
        'form': form,
    }

    return render(request, 'login.html', context)



@login_required(login_url='/')
def dashboard(request):
    client_form = ClientForm
    item_form = ItemForm
    clients = Client.objects.all()
    count = clients.count()
    context = {
        'clients': clients,
        'count': count,
        'client_form': client_form,
        'item_form': item_form
    }

    return render(request, 'index.html', context)


@login_required(login_url='/')
def all_client_list(request):
    client_form = ClientForm
    item_form = ItemForm

    if request.method=='GET':
        clients = Client.objects.all()

        context = {
            'clients':clients,
            'client_form': client_form,
            'item_form': item_form
        }
        return render(request, 'components/client_list.html', context)


@login_required(login_url='/')
def all_item_list(request):
    client_form = ClientForm
    item_form = ItemForm
    
    if request.method=='GET':
        items = Item.objects.all()


        context = {
            'items': items,
            'client_form': client_form,
            'item_form': item_form
        }
        
        return render(request, 'components/item_list.html', context)