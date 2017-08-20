from django.forms import ModelForm
from django.contrib.auth.models import User


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')