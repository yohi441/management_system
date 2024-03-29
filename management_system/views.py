from ast import Try
from multiprocessing import context
from django.shortcuts import redirect, render
from django.urls import reverse
from management_system.models import Client, Item, Transaction, Category, Forfeit
from django.contrib.auth import logout
from django.contrib.auth import login
from management_system.forms import LoginForm, ClientForm, ItemForm, TransactionForm
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
import datetime
from django.core.paginator import Paginator


def category_list(category_model):
    categories = category_model.objects.all()
    return categories

def five_days_due_date(model):
    transactions = model.objects.filter(
        Q(status='Renew') | Q(status='New'))

    e_list = []

    for transaction in transactions:
        expiration = transaction.due_date
        date_now = datetime.datetime.now().date()
        days = (expiration) - date_now

        if days.days <= 5 and days.days >= 0:
            e_list.append(transaction.id)

    five_days_before_expire = model.objects.filter(pk__in=e_list)

    return five_days_before_expire


def pending_check(model):
    t = model.objects.filter(Q(status='Renew') | Q(status='New'))
    date_now = datetime.datetime.now().date()
    counter = 0
    if t:
        for i in t:
            if date_now > i.due_date:
                i.status = 'Pending'
                i.save()
                counter += 1

    return counter


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'components/client_detail.html'
    model = Client

    transactions = five_days_due_date(Transaction)

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['count_notification'] = len(self.transactions)
        context['categories'] = category_list(Category)

        return context


client_detail_view = ClientDetailView.as_view()


# class ItemDetailView(LoginRequiredMixin, DetailView):
#     template_name = 'components/item_detail.html'
#     model = Item

#     def get_context_data(self, **kwargs):
#         context = super(ItemDetailView, self).get_context_data(**kwargs)
#         transactions = five_days_due_date(Transaction)
#         context['count_notification'] = len(transactions)
#         context['categories'] = category_list(Category)

#         return context
class ItemDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        template_name = 'components/item_detail.html'
        try:
            item = Item.objects.get(pk=pk)
            context = {
                'object': item,
            }
            return render(request, template_name, context)
        except:
            messages.error(request, 'The current item dont have related transaction')
            return redirect(reverse('all_item_list'))


item_detail_view = ItemDetailView.as_view()


class TransactionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'components/transaction_detail.html'
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super(TransactionDetailView, self).get_context_data(**kwargs)
        transactions = five_days_due_date(Transaction)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)

        return context


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
        new = Transaction.objects.filter(status='New').count()
        pending = Transaction.objects.filter(status='Pending').count()
        renew = Transaction.objects.filter(status='Renew').count()
        pending_check(Transaction)
        transaction = five_days_due_date(Transaction)
        categories = category_list(Category)

        context = {
            'clients': clients,
            'count': count,
            'new': new,
            'pending': pending,
            'total_renew': renew,
            'count_notification': len(transaction),
            'categories': categories
        }

        return render(request, 'index.html', context)


dashboard_view = DashboardView.as_view()


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list_full.html"
    paginate_by = 10
    context_object_name = 'clients'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        transactions = five_days_due_date(Transaction)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)


        return context


client_list_view = ClientListView.as_view()


class ItemListView(LoginRequiredMixin, ListView):
    queryset = Item.objects.filter(status="A")
    template_name = "item_list_full.html"
    paginate_by = 10
    context_object_name = 'items'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        transactions = five_days_due_date(Transaction)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)

        return context


item_list_view = ItemListView.as_view()


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transaction_list_full.html"
    paginate_by = 10
    context_object_name = 'transactions'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        transactions = five_days_due_date(Transaction)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)

        return context


transaction_list_view = TransactionListView.as_view()


class TransactionListPendingView(LoginRequiredMixin, ListView):

    queryset = Transaction.objects.filter(status="Pending")
    template_name = "transaction_pending_list.html"
    paginate_by = 10
    context_object_name = 'transactions'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(TransactionListPendingView,
                        self).get_context_data(**kwargs)
        transactions = five_days_due_date(Transaction)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)

        return context


transaction_list_pending_view = TransactionListPendingView.as_view()


class TransactionListPaidView(LoginRequiredMixin, ListView):

    queryset = Transaction.objects.filter(status="Paid")
    template_name = "transaction_paid_list.html"
    paginate_by = 10
    context_object_name = 'transactions'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(TransactionListPaidView,
                        self).get_context_data(**kwargs)
        transactions = five_days_due_date(Transaction)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)

        return context


transaction_list_paid_view = TransactionListPaidView.as_view()


class TransactionListRenewView(LoginRequiredMixin, ListView):

    queryset = Transaction.objects.filter(status="Renew")
    template_name = "transaction_renew_list.html"
    paginate_by = 10
    context_object_name = 'transactions'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(TransactionListRenewView,
                        self).get_context_data(**kwargs)
        transactions = five_days_due_date(Transaction)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)

        return context


transaction_list_renew_view = TransactionListRenewView.as_view()


class TransactionListNewView(LoginRequiredMixin, ListView):

    queryset = Transaction.objects.filter(status="New")
    template_name = "transaction_new_list.html"
    paginate_by = 10
    context_object_name = 'transactions'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(TransactionListNewView,
                        self).get_context_data(**kwargs)
        transactions = five_days_due_date(Transaction)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)

        return context


transaction_list_new_view = TransactionListNewView.as_view()


class ItemFormView(LoginRequiredMixin, View):

    def get(self, request):
        form = ItemForm()
        transactions = five_days_due_date(Transaction)
        context = {
            'form': form,
            'count_notification': len(transactions),
            'categories': category_list(Category)
        }

        return render(request, 'components/item_form.html', context)

    def post(self, request):
        form = ItemForm(request.POST)
        transactions = five_days_due_date(Transaction)
        context = {
            'form': form,
            'count_notification': len(transactions),
            'categories': category_list(Category)
        }

        if form.is_valid():
            form.save()
            form = ItemForm()
            context = {
                'form': form,
                'count_notification': len(transactions),
                'categories': category_list(Category)
            }
            messages.success(request, "Item Add Successfully")
            return render(request, 'components/item_form.html', context)

        return render(request, 'components/item_form.html', context)


item_form_view = ItemFormView.as_view()


class ClientFormView(LoginRequiredMixin, View):

    def get(self, request):
        form = ClientForm()
        transactions = five_days_due_date(Transaction)
        context = {
            'form': form,
            'count_notification': len(transactions),
            'categories': category_list(Category)
        }

        return render(request, 'components/client_form.html', context)

    def post(self, request):
        form = ClientForm(request.POST)
        transactions = five_days_due_date(Transaction)
        context = {
            'form': form,
            'count_notification': len(transactions),
            'categories': category_list(Category)
        }

        if form.is_valid():
            form.save()
            form = ClientForm()
            context = {
                'form': form,
                'count_notification': len(transactions),
                'categories': category_list(Category)
            }
            messages.success(request, "Client Add Successfully")
            return render(request, 'components/client_form.html', context)

        return render(request, 'components/client_form.html', context)


client_form_view = ClientFormView.as_view()


class TransactionFormView(LoginRequiredMixin, View):

    def get(self, request):
        form = TransactionForm()
        transactions = five_days_due_date(Transaction)
        context = {
            'form': form,
            'count_notification': len(transactions),
            'categories': category_list(Category)
        }

        return render(request, 'components/transaction_form.html', context)

    def post(self, request):
        form = TransactionForm(request.POST)
        transactions = five_days_due_date(Transaction)

        context = {
            'form': form,
            'count_notification': len(transactions),
            'categories': category_list(Category)
        }

        if form.is_valid():
            form.save()
            form = TransactionForm()
            context = {
                'form': form,
                'count_notification': len(transactions),
                'categories': category_list(Category)
            }
            messages.success(request, "Transaction Add Successfully")
            return render(request, 'components/transaction_form.html', context)

        return render(request, 'components/transaction_form.html', context)


transaction_form_view = TransactionFormView.as_view()


class ClientUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        form = ClientForm(instance=client)
        context = {
            'form': form, 
            'client': client,
            'categories': category_list(Category)
            }
        return render(request, 'components/client_update.html', context)

    def post(self, request, pk):
        client = Client.objects.get(pk=pk)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client Updated Successfully")
            return redirect(reverse('client_detail', kwargs={'pk': pk}))
        context = {
            'form': form,
            'client': client,
            'categories': category_list(Category)
            }
        return render(request, 'components/client_update.html', context)


client_update_view = ClientUpdateView.as_view()


class ItemUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        form = ItemForm(instance=item)
        context = {
            'form': form, 
            'item': item,
            'categories': category_list(Category)
            }
        return render(request, 'components/item_update.html', context)

    def post(self, request, pk):
        item = Item.objects.get(pk=pk)
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item Updated Successfully")
            return redirect(reverse('item_detail', kwargs={'pk': pk}))
        context = {
            'form': form, 
            'item': item,
            'categories': category_list(Category)
            }
        return render(request, 'components/item_update.html', context)


item_update_view = ItemUpdateView.as_view()


class TransactionUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        form = TransactionForm(instance=transaction)
        context = {
            'form': form, 
            'transaction': transaction,
            'categories': category_list(Category)
            }
        return render(request, 'components/transaction_update.html', context)

    def post(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction Updated Successfully")
            return redirect(reverse('transaction_detail', kwargs={'pk': pk}))
        context = {
            'form': form, 
            'transaction': transaction,
            'categories': category_list(Category)
            }
        return render(request, 'components/transaction_update.html', context)


transaction_update_view = TransactionUpdateView.as_view()


class SearchResultsView(LoginRequiredMixin, View):

    def get(self, request):
        q = request.GET.get('q')
        clients = Client.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(middle_name__icontains=q)
        )[:10]

        transactions = five_days_due_date(Transaction)

        context = {
            'clients': clients,
            'count_notification': len(transactions),
            'categories': category_list(Category)
        }

        return render(request, 'components/search_results.html', context)

    def post(self, request):
        pass


search_results_view = SearchResultsView.as_view()


class RenewTransactionView(View):

    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)

        transaction.month += 1

        if datetime.datetime.now().date() > transaction.due_date:
            transaction.status = 'Pending'
        else:
            transaction.status = 'Renew'

        transaction.save()
        context = {
            'categories': category_list(Category)
        }
        return redirect(reverse('transaction_detail', kwargs={'pk': pk}), context)


renew_transaction_view = RenewTransactionView.as_view()


class PaidTransactionView(View):

    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        item_pk = transaction.item.id
        item = Item.objects.get(pk=item_pk)
        item.status = 'I'
        item.save()
        transaction.status = 'Paid'
        transaction.save()

        context = {
            'categories': category_list(Category)
        }
        return redirect(reverse('transaction_detail', kwargs={'pk': pk}), context)


paid_transaction_view = PaidTransactionView.as_view()


class ForfeitItem(View):
    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        item_pk = transaction.item.id
        item = Item.objects.get(pk=item_pk)
        item.status = 'I'
        transaction.status = 'Forfeit'
    
        transaction.save()
        item.save()
        obj = Forfeit.objects.create(item=item)
        obj.save()

        context = {
            'categories': category_list(Category)
        }

        return redirect(reverse('transaction_detail', kwargs={'pk': pk}), context)

forfeit_item = ForfeitItem.as_view()



class FiveDaysBeforeDueDate(LoginRequiredMixin, ListView):
    template_name = 'five_days_before_due_date.html'

    transactions = five_days_due_date(Transaction)
    queryset = transactions
    paginate_by = 10
    context_object_name = 'transactions'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(FiveDaysBeforeDueDate, self).get_context_data(**kwargs)
        context['count_notification'] = len(self.transactions)
        context['categories'] = category_list(Category)

        return context


five_days_before_due_date = FiveDaysBeforeDueDate.as_view()


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "partials/category_partial.html"
    context_object_name = "items"
    paginate_by = 10
    model = Item
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        context['categories'] = category_list(Category)

        return context

    def get_queryset(self):
        return super(CategoryListView, self).get_queryset().filter(category=self.kwargs['pk'])


category_list_view = CategoryListView.as_view()


class ForfeitItemsView(LoginRequiredMixin, ListView):
    template_name = "forfeit_item_list_full.html"
    context_object_name = "items"
    paginate_by = 10
    model = Forfeit
    ordering = ['item']
    transactions = five_days_due_date(Transaction)

    def get_context_data(self, **kwargs):
        context = super(ForfeitItemsView, self).get_context_data(**kwargs)
        context['count_notification'] = len(self.transactions)
        context['categories'] = category_list(Category)

        return context

forfeit_items_view = ForfeitItemsView.as_view()


class ItemCategoriesNameList(LoginRequiredMixin, ListView):
    template_name = 'item_category_name_list.html'
    context_object_name = 'transactions'
    paginate_by = 10


    def get_queryset(self, **kwargs):
        items = Item.objects.filter(category=self.kwargs.get('pk'))
        transaction_list = []
        for item in items:
            transaction_list.append(item.pk)
        transactions = Transaction.objects.filter(item__in=transaction_list)
        return transactions

    def get_context_data(self, **kwargs):
        transactions = five_days_due_date(Transaction)
        category = Category.objects.get(pk=self.kwargs.get('pk'))
        context = super(ItemCategoriesNameList, self).get_context_data(**kwargs)
        context['count_notification'] = len(transactions)
        context['categories'] = category_list(Category)
        context['category'] = category

        return context
    

item_categories_name_list = ItemCategoriesNameList.as_view()
    
