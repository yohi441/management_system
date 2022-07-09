from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from management_system.models import Client, Item




class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = "__all__"



class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = "__all__"

class LoginForm(AuthenticationForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'password':
                self.fields[field].widget = forms.widgets.PasswordInput(attrs={
                    'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                    'placeholder': field.capitalize,
                })
            else:
                self.fields[field].widget = forms.widgets.TextInput(attrs={
                    'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                    'placeholder': field.capitalize,
                })


    



