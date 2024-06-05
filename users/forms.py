from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import get_user_model


class RegistrationForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]
