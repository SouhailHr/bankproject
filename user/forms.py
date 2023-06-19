from django.contrib.auth import forms, get_user_model, password_validation
from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.utils.translation import gettext_lazy as _
from user.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_picture', 'address',
            'phone_number')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserUpdateForm(django_forms.ModelForm):
    password1 = django_forms.CharField(
        label=_("Password"),
        strip=False,
        widget=django_forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = django_forms.CharField(
        label=_("Password confirmation"),
        widget=django_forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['profile_picture']

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_picture', 'address',
            'phone_number')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    username = django_forms.CharField(
        label=_("Username"),
        max_length=150,
        widget=django_forms.TextInput(attrs={'autofocus': True}),
    )
    password = django_forms.CharField(
        label=_("Password"),
        strip=False,
        widget=django_forms.PasswordInput,
    )
