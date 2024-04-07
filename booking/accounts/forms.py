from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.contrib.auth import forms as auth_forms

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
