from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from management_system.models import Client, Item
from django.contrib.auth import logout
from django.contrib.auth import login
from management_system.forms import LoginForm, ClientForm, ItemForm
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


logout_view = LogoutView.as_view()


class LoginView(View):

    def get(self, request):
        form = LoginForm(request)
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))

        context = {
            'form': form,
        }

        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('dashboard'))

        context = {
            'form': form,
        }

        return render(request, 'login.html', context)


login_view = LoginView.as_view()


class DashboardView(View, LoginRequiredMixin):

    def get(self, request):
        clients = Client.objects.all().order_by('-created')[:10]
        count = clients.count()

        context = {
            'clients': clients,
            'count': count,
        }

        return render(request, 'index.html', context)


dashboard_view = DashboardView.as_view()


class ClientListView(ListView, LoginRequiredMixin):
    model = Client
    template_name = "client_list_full.html"
    paginate_by = 10
    context_object_name = 'clients'
    ordering = ['-created']


client_list_view = ClientListView.as_view()


class ItemListView(ListView, LoginRequiredMixin):
    model = Item
    template_name = "item_list_full.html"
    paginate_by = 10
    context_object_name = 'items'
    ordering = ['-created']



item_list_view = ItemListView.as_view()


class ItemFormView(View, LoginRequiredMixin):

    def get(self, request):
        form = ItemForm()

        return render(request, 'components/item_form.html', {'form': form})

    def post(self, request):
        form = ItemForm(request.POST)

        if form.is_valid():
            form.save()
            form = ItemForm()
          
            return render(request, 'components/item_form.html', {'form': form})

        return render(request, 'components/item_form.html', {'form': form})


item_form_view = ItemFormView.as_view()


class ClientFormView(View, LoginRequiredMixin):

    def get(self, request):
        form = ClientForm()

        return render(request, 'components/client_form.html', {'form': form})

    def post(self, request):
        form = ClientForm(request.POST)

        if form.is_valid():
            form.save()
            form = ClientForm()
          
            return render(request, 'components/client_form.html', {'form': form})

        return render(request, 'components/client_form.html', {'form': form})


client_form_view = ClientFormView.as_view()
