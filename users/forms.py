from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password

from .models import CustomUser
from odds.models import Bookmaker


class AdminUserChange(forms.ModelForm):
    CHOICES = (
        ('draftkings', 'DraftKings'),
        ('fanduel', 'FanDuel'),
        ('pointsbetus', 'PointBet'),
        ('betmgm', 'BetMGM'),
        ('barstool', 'Barstool'),
    )
    bookmakers = forms.MultipleChoiceField(choices=CHOICES, widget=forms.widgets.CheckboxSelectMultiple)
    old_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password_confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(AdminUserChange, self).__init__(*args, **kwargs)
        self.initial['bookmakers'] = CustomUser.objects.filter(email=self.instance)[0].bookmakers.split(",")

    def clean_bookmakers(self):
        """ Convert list to comma separated string """
        data = self.cleaned_data["bookmakers"]
        data_as_string = ",".join(data)
        return data_as_string

    def clean_new_password_confirm(self):
        """ Verify passwords match """
        cleaned_data = super().clean()
        old = cleaned_data.get("old_password")
        new = cleaned_data.get("new_password")
        confirm = cleaned_data.get("new_password_confirm")
        if old or new or confirm:
            if not old:
                self.add_error("old_password", "Your password is not correct")
            if not new:
                self.add_error("new_password", "A new password is required")
            if not confirm:
                self.add_error("new_password_confirm", "A new password is required")
            if old and new and confirm:
                if not check_password(old, CustomUser.objects.filter(email=self.instance)[0].password):
                    self.add_error("old_password", "Your password is not correct")
                    return new
                if new != confirm:
                    self.add_error("new_password_confirm", "Your passwords must match")
                    return new
                if check_password(new, CustomUser.objects.filter(email=self.instance)[0].password):
                    self.add_error("new_password", "Your new passsword cannot be the same as the old one")
        return new
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'old_password', 'new_password', 'new_password_confirm', 'bookmakers')


class AdminUserCreation(forms.ModelForm):
    CHOICES = (
        ('draftkings', 'DraftKings'),
        ('fanduel', 'FanDuel'),
        ('pointsbetus', 'PointBet'),
        ('betmgm', 'BetMGM'),
        ('barstool', 'Barstool'),
    )
    bookmakers = forms.MultipleChoiceField(choices=CHOICES, widget=forms.widgets.CheckboxSelectMultiple, required=True)
    first_name = forms.CharField(max_length=50, required=True, label="First Name")
    last_name = forms.CharField(max_length=50, required=True, label="Last Name")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)

    def clean_bookmakers(self):
        """ Convert list to comma separated string """
        data = self.cleaned_data["bookmakers"]
        data_as_string = ",".join(data)
        return data_as_string

    def clean_password_confirm(self):
        """ Verify passwords match """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password_confirm")
        if password1 and password2 and password1 != password2:
            self.add_error("password_confirm", "Your passwords must match")
        return password1

    def save(self, commit=True):
        """ Add the new user """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password', 'password_confirm', 'bookmakers')


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": ""
        })
        self.fields["password"].widget.attrs.update({
            "class": ""
        })
