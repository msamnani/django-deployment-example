from django import forms
from first_app.models import UserProfileInfo, FirstAppUser
from django.core import validators
from django.contrib.auth.models import User


# you can create your own validator
def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("NAME NEEDS TO START WITH Z")

class FormName(forms.Form):
    name = forms.CharField(validators=[check_for_z])
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Enter you email again')
    text = forms.CharField(widget=forms.Textarea)
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput)
    # you can use build in validators
    botcatcher2 = forms.CharField(required=False, widget=forms.HiddenInput,validators=[validators.MaxLengthValidator(0)])

    # you can do a manual check on individual fields
    def clean_botcatcher(self):
        botcatcher = self.cleaned_data['botcatcher']
        if len(botcatcher) > 0:
            raise forms.ValidationError("GOTCHA BOT!")
        return botcatcher

    # you can do a manual check on all fields in the form
    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']

        if email != vmail:
            raise forms.ValidationError("MAKE SURE EMAILS MATCH")

class NewUserForm(forms.ModelForm):
    class Meta:
        model =  FirstAppUser
        fields = "__all__"

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')