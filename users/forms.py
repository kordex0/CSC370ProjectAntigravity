from django import forms
from users.models import User

class NewUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)  
    first_name = forms.CharField(label='First Name', max_length=30)  
    last_name = forms.CharField(label='Last Name', max_length=30)  
    password = forms.CharField(label='Password', max_length=30)  
    password_retyped = forms.CharField(label='Password (type again)', max_length=30)  

    role = forms.ChoiceField(label='User role', choices=User.ROLE_CHOICES)


