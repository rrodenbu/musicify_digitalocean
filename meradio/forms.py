from django import forms
from django.contrib.auth.models import User

from meradio.models import Profile
from meradio.models import *

# Used to present, check and validate the Update Account Form
class AccountSettingsForm(forms.Form):
    first_name = forms.CharField(max_length=200,
                                 label='First Name',
                                 required=False)
    last_name = forms.CharField(max_length=200,
                                 label='Last Name',
                                 required=False)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(max_length=200,
                                label='New Password',
                                widget=forms.PasswordInput(),
                                required=False)
    password2 = forms.CharField(max_length=200,
                                label='Confirm Password',
                                widget=forms.PasswordInput(),
                                required=False)
    description = forms.CharField(max_length=140,
                                  required=False)
    avatar = forms.ImageField(required = False)

    # Customize form validation for properties that apply to more
    # than one field. Override the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(AccountSettingsForm, self).clean()

        # Confirm that password and password confirmation are the same
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords did not match.')

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

# Used to present, check, and validate the Registration form
class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=200,
                                 label='First Name')
    last_name = forms.CharField(max_length=200,
                                label='Last Name')
    email = forms.EmailField()
    username = forms.CharField(max_length=200)
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,
                                label='Confirm Password',
                                widget=forms.PasswordInput())

    # Customize form validation for properties that apply to more
    # than one field. Override the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirm that password and password confirmation are the same
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords did not match.')

        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).count() == 0:
            raise forms.ValidationError('There is another account under this email address.')

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError('Username is already taken.')

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username


# Use this to handle extra information about user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'description', 'liked', 'disliked',
                   'favorites', 'password_temp', 'preferences',
                   'status', 'song', 'start_time', 'pause_duration')
        widgets = {'avatar': forms.FileInput(), 'token': forms.HiddenInput()}

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        return cleaned_data


# Used to present, check and validate the Update Description Form
class DescriptionForm(forms.Form):
    description = forms.CharField(max_length=120,
                                  label='Description',
                                  required=False)

    # Customize form validation for properties that apply to more                                                                                                        
    # than one field. Override the forms.Form.clean function.                                                                                                            
    def clean_description(self):
        cleaned_data = super(DescriptionForm, self).clean()
        # If empty, use empty string
        description = cleaned_data.get('description')
        if not description:
            description = ""

        # Generally return the cleaned data we got from the cleaned_data                                                                                   # dictionary   
        return description


class SendEmailForm(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        # Confirms that the username is present in the User model database.
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__exact=email):
            raise forms.ValidationError('Email is not affiliated with an account')

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return email


# This form displays the fields and checks input for resetting a user password
class ForgetPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=200,
                                label='New Password',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,
                                label='Confirm Password',
                                widget=forms.PasswordInput())

    # Customize form validation for properties that apply to more
    # than one field. Override the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ForgetPasswordForm, self).clean()

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    def clean_password2(self):
        cleaned_data = super(ForgetPasswordForm, self).clean()
        # Confirm that password and password confirmation are the same
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password confirmation did not match.')
