from dataclasses import fields
from pyexpat import model
from secrets import choice
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from management_system.models import Client, Item, Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        for field in self.fields:
            if field == 'date_pawned' or field == 'redeem_date':
                self.fields[str(field)].widget = forms.SelectDateWidget(attrs={
                    'class': 'rounded-md mb-2 block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-blue-400 focus:outline-none focus:ring-0 focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
        
                })
            else:
                self.fields[str(field)].widget.attrs.update({
                    'class': 'rounded-md mb-2 block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-blue-400 focus:outline-none focus:ring-0 focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                    'placeholder': str(field).replace('_', ' ').capitalize(),
                })

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({
                'class': 'rounded-md mb-2 block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-blue-400 focus:outline-none focus:ring-0 focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': str(field).replace('_', ' ').capitalize(),
            })
           



class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'rounded-md block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-blue-400 focus:outline-none focus:shadow-outline-blue focus:ring-0 dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': field.replace('_', ' ').capitalize(),
                })

class LoginForm(AuthenticationForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'rounded-md block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:ring-0 focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray',
                'placeholder': field.replace('_', ' ').capitalize(),
                })


    



