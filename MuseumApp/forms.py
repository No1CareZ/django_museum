from django import forms
from .models import User


class ProfileEditForm(forms.ModelForm):

    class Meta():
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )
