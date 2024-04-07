from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.contrib.auth import forms as auth_forms

from booking.accounts.models import Profile

UserModel = get_user_model()


class BookingUserCreationForm(auth_forms.UserCreationForm):
    user = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email', 'password1', 'password2')


class BookingChangeForm(auth_forms.UserChangeForm):

    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ('first_name', 'last_name', 'date_of_birth', 'money')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class DeleteProfileForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('email', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.check_password(password):
            raise forms.ValidationError('Incorrect password')
        return password
