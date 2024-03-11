from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


# Signup Form
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

# LOGIN
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

#USER MODEL
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


#password reset
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')


#Parentchild register
from django import forms
from .models import Family

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'  # Include all fields from the Family model

#immunization schedule
class ImmunizationScheduleForm(forms.ModelForm):
    class Meta:
        model = ImmunizationSchedule
        fields = ['vaccine_name', 'recommended_age', 'number_of_doses', 'additional_info', 'child_name', 'child_image']
        labels = {
            'vaccine_name': 'Vaccine Name',
            'recommended_age': 'Recommended Age (months)',
            'number_of_doses': 'Number of Doses',
            'additional_info': 'Additional Information (optional)',
            'child_name': 'Child Name',
            'child_image': 'Child Image'
        }
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 3}),  # Textarea widget for additional_info field
        }


# Reminder settings
class ReminderSettingsForm(forms.ModelForm):
    class Meta:
        model = ReminderSettings
        fields = ['email_reminder', 'sms_reminder', 'event_date']  # Include the event date field
        labels = {
            'email_reminder': 'Email Reminder',
            'sms_reminder': 'SMS Reminder',
            'event_date': 'Event Date',  # Label for the event date field
        }
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),  # Use a date input widget for the event date field
        }
