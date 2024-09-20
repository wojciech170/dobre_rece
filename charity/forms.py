import django.forms as forms

from django.contrib.auth.models import User


class EditUserForm(forms.ModelForm):
    current_password = forms.CharField(
        label='Aktualne Hasło',
        widget=forms.PasswordInput,
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Hasło się nie zgadza")
        return current_password


class ChangePasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label='Nowe Hasło',
        widget=forms.PasswordInput,
        required=True
    )
    new_password2 = forms.CharField(
        label='Potwierdz nowe hasło',
        widget=forms.PasswordInput,
        required=True
    )
    old_password = forms.CharField(
        label='Aktualne hasło',
        widget=forms.PasswordInput,
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Aktualne hasło jest niepoprawne.")
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError("Nowe hasła są różne.")
        return new_password2

    def save(self, commit=True):
        new_password = self.cleaned_data.get('new_password1')
        self.user.set_password(new_password)
        if commit:
            self.user.save()
