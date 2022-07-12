from email import message
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from management_system.models import Client, Item, Transaction
from django.contrib.auth import logout
from django.contrib.auth import login
from management_system.forms import LoginForm, ClientForm, ItemForm, TransactionForm
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from time import sleep



class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'components/client_detail.html'
    model = Client

client_detail_view = ClientDetailView.as_view()


class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = 'components/item_detail.html'
    model = Item

item_detail_view = ItemDetailView.as_view()


class TransactionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'components/transaction_detail.html'
    model = Transaction

transaction_detail_view = TransactionDetailView.as_view()


class LogoutView(LoginRequiredMixin, View):
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


class DashboardView(LoginRequiredMixin, View):

    def get(self, request):
        clients = Client.objects.all().order_by('-created')[:10]
        count = Client.objects.all().count()
        
        context = {
            'clients': clients,
            'count': count,
        }

        return render(request, 'index.html', context)


dashboard_view = DashboardView.as_view()


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list_full.html"
    paginate_by = 10
    context_object_name = 'clients'
    ordering = ['-created']


client_list_view = ClientListView.as_view()


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "item_list_full.html"
    paginate_by = 10
    context_object_name = 'items'
    ordering = ['-created']

item_list_view = ItemListView.as_view()


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transaction_list_full.html"
    paginate_by = 10
    context_object_name = 'transactions'
    ordering = ['-created']


transaction_list_view = TransactionListView.as_view()



class ItemFormView(LoginRequiredMixin, View):

    def get(self, request):
        form = ItemForm()

        return render(request, 'components/item_form.html', {'form': form})

    def post(self, request):
        form = ItemForm(request.POST)

        if form.is_valid():
            form.save()
            form = ItemForm()
            messages.success(request, "Item Add Successfully")
            return render(request, 'components/item_form.html', {'form': form})

        return render(request, 'components/item_form.html', {'form': form})


item_form_view = ItemFormView.as_view()


class ClientFormView(LoginRequiredMixin, View):

    def get(self, request):
        form = ClientForm()

        return render(request, 'components/client_form.html', {'form': form})

    def post(self, request):
        form = ClientForm(request.POST)

        if form.is_valid():
            form.save()
            form = ClientForm()
            messages.success(request, "Client Add Successfully")
            return render(request, 'components/client_form.html', {'form': form})

        return render(request, 'components/client_form.html', {'form': form})


client_form_view = ClientFormView.as_view()


class TransactionFormView(LoginRequiredMixin, View):

    def get(self, request):
        form = TransactionForm()

        return render(request, 'components/transaction_form.html', {'form': form})

    def post(self, request):
        form = TransactionForm(request.POST)

        if form.is_valid():
            form.save()
            form = TransactionForm()
            messages.success(request, "Transaction Add Successfully")
            return render(request, 'components/transaction_form.html', {'form': form})

        return render(request, 'components/transaction_form.html', {'form': form})

transaction_form_view = TransactionFormView.as_view()



class ClientUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        form = ClientForm(instance=client)
        return render(request, 'components/client_update.html', {'form' : form, 'client':client})

    def post(self, request, pk):
        client = Client.objects.get(pk=pk)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client Updated Successfully")
            return redirect(reverse('client_detail', kwargs={'pk': pk}))
        return render(request, 'components/client_update.html', {'form': form, 'client':client})

client_update_view = ClientUpdateView.as_view()


class ItemUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        form = ItemForm(instance=item)
        return render(request, 'components/item_update.html', {'form' : form, 'item':item})

    def post(self, request, pk):
        item = Item.objects.get(pk=pk)
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item Updated Successfully")
            return redirect(reverse('item_detail', kwargs={'pk': pk}))
        return render(request, 'components/item_update.html', {'form': form, 'item':item})

item_update_view = ItemUpdateView.as_view()


class TransactionUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        form = TransactionForm(instance=transaction)
        return render(request, 'components/transaction_update.html', {'form' : form, 'transaction':transaction})

    def post(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction Updated Successfully")
            return redirect(reverse('transaction_detail', kwargs={'pk': pk}))
        return render(request, 'components/transaction_update.html', {'form': form, 'transaction':transaction})

transaction_update_view = TransactionUpdateView.as_view()


