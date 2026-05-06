"""
========================================================
  accounts/forms.py
  STEP 3: Django Forms
========================================================

WHY FORMS?
  Django Forms do 3 things automatically:
    1. Render HTML input fields in templates ({{ form.email }})
    2. Validate user input (is email valid? password match?)
    3. Return cleaned data ready to save to database

  WITHOUT forms: you'd write validation logic yourself in every view.
  WITH forms: validation is centralized, reusable, and clean.

FORMS vs SERIALIZERS:
  Forms       → Used with HTML templates (browser submits data)
  Serializers → Used with DRF APIs (Postman / React sends JSON)
  Both do validation — just for different input types.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import EmployerProfile, CandidateProfile

User = get_user_model()  # Returns our custom User model


# ─── REGISTRATION FORM ────────────────────────────────────────────────────────
class RegisterForm(forms.ModelForm):
    """
    Used in the HTML registration page.
    ModelForm automatically creates fields from the User model.
    """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'role':       forms.Select(),
        }

    def clean_email(self):
        """
        WHY clean_<fieldname>: Custom validation for a specific field.
        This runs automatically when form.is_valid() is called.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        """
        WHY clean(): Cross-field validation (comparing two fields).
        Called after all individual field clean methods.
        """
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        """
        Override save() to hash the password before saving.
        NEVER save plain text passwords — always use set_password().
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Auto-create the corresponding profile
            if user.is_employer:
                EmployerProfile.objects.create(user=user, company_name='My Company')
            else:
                CandidateProfile.objects.create(user=user)
        return user


# ─── LOGIN FORM ───────────────────────────────────────────────────────────────
class LoginForm(AuthenticationForm):
    """
    WHY inherit AuthenticationForm?
    Django's AuthenticationForm already handles:
      - Checking if credentials are correct
      - Checking if account is active
    We just customize the widget styles.
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'autofocus': True}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )


# ─── EMPLOYER PROFILE FORM ────────────────────────────────────────────────────
class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_website', 'company_size', 'industry',
                  'company_description', 'company_logo']
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
        }


# ─── CANDIDATE PROFILE FORM ───────────────────────────────────────────────────
class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['resume', 'skills', 'experience_years', 'current_job_title',
                  'linkedin_url', 'github_url']
        widgets = {
            'skills': forms.TextInput(attrs={'placeholder': 'Python, Django, React, SQL'}),
        }