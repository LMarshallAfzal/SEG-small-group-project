from django import forms
from django.core.validators import RegexValidator
from .models import User

class LogInForm(forms.Form):
    email = forms.EmailField(label = "Email")
    password = forms.CharField(label = "Password", widget = forms.PasswordInput())

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'experience_level', 'personal_statement']
        widgets = { 'bio': forms.Textarea() }

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'experience_level', 'personal_statement']
        widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea() }

    new_password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(),
        validators = [RegexValidator(
            regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message = 'Password must contain an uppercase character, a lowercase '
                      'character and a number'
        )]
    )
    password_confirmation = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput())
    

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio','experience_level','personal_statement']
        widgets = { 'bio': forms.Textarea() }

    def clean(self):
        super().clean()
        self.cleaned_data
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'password confirmation does not match password.')

    def save(self):
        super().save(commit = False)
        user = User.objects.create_user(
            username = self.cleaned_data.get('email'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            bio = self.cleaned_data.get('bio'),
            experience_level = self.cleaned_data.get('experience_level'),
            personal_statement = self.cleaned_data.get('personal_statement'),
            password = self.cleaned_data.get('new_password'),
        )
        return user
