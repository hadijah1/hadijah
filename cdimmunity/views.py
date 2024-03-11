from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth.models import User


#RESET PASS1
def send_password_reset_email(request, email):
    # Check if the email exists in the database
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Handle the case where the email does not exist
        messages.error(request, 'User with this email does not exist.')
        return None

    # Generate a password reset token
    token = default_token_generator.make_token(user)

    # Encode the user's ID and token to be included in the URL
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Construct the password reset URL
    reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))

    # Render the email template with the reset URL
    email_subject = 'Password Reset'
    email_body = render_to_string('password_reset_email.html', {'reset_url': reset_url})

    # Send the email
    send_mail(email_subject, email_body, 'enote7y@gmail.com', [email])

#SIGNINUP
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form submission
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            user.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
        

#LOGIN USER
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)  # Correct usage of login() function
                # Redirect to the page user was trying to access, or home page if no next parameter
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    # If the next parameter exists, pass it to the template to display a message
    next_param = request.GET.get('next')
    return render(request, 'login.html', {'form': form, 'next_param': next_param})

@login_required
def home(request):
    # Filter Family objects based on the currently logged-in user
    families = Family.objects.filter(email=request.user.email)
    return render(request, 'home.html', {'families': families})

def index (request):
    return render(request, 'index.html')

@login_required
def cldreg_success (request):
    return render(request, 'cldreg_success.html')

@login_required
def rm_suc (request):
    return render(request, 'rm_suc.html')

#child register
from .forms import FamilyForm

@login_required
def cldreg(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cldreg_success')  # Redirect to success page
    else:
        form = FamilyForm()
    return render(request, 'cldreg.html', {'form': form})

#immunization schedule
@login_required
def immunization_schedule(request):
    if request.method == 'POST':
        form = ImmunizationScheduleForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            # Save the form instance without committing to the database yet
            schedule = form.save(commit=False)
            # Manually set the child image field with the uploaded file
            schedule.child_image = request.FILES.get('child_image')
            # Save the form instance to the database
            schedule.save()
            # Redirect to a success page or wherever appropriate
            return redirect('view_schedule')
    else:
        form = ImmunizationScheduleForm()
    return render(request, 'immunization_schedule.html', {'form': form})


@login_required
def view_schedule(request):
    query = request.GET.get('search')
    if query:
        immunization_schedule = ImmunizationSchedule.objects.filter(
            Q(child_name__icontains=query) |
            Q(vaccine_name__icontains=query)
        )
    else:
        immunization_schedule = ImmunizationSchedule.objects.all()

    return render(request, 'view_schedule.html', {'immunization_schedule': immunization_schedule})

#Logout
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('index')  

#Reminder settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.timezone import now
# Add necessary imports
from django.http import HttpResponseNotAllowed, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def remind(request):
    # Retrieve or create reminder settings for the current user
    reminder_settings, created = ReminderSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ReminderSettingsForm(request.POST, instance=reminder_settings)
        if form.is_valid():
            # Save the updated reminder settings
            form.save()

            # Check if email reminder is enabled
            if reminder_settings.email_reminder:
                try:
                    # Prepare email content
                    subject = 'Reminder Settings Updated'
                    current_site = get_current_site(request)
                    context = {
                        'user': request.user,
                        'domain': current_site.domain,
                        'settings_url': reverse('remind'),  # Assuming this is the URL to the reminder settings page
                    }
                    html_message = render_to_string('reminder_settings_updated.html', context)
                    plain_message = strip_tags(html_message)

                    # Send email notification
                    send_mail(
                        subject,
                        plain_message,
                        'enote7y@gmail.com',  # Replace with your email sender
                        [request.user.email],  # Send email to the user
                        html_message=html_message,
                    )
                except Exception as e:
                    # Log or print the exception for debugging
                    print(f"Error sending email: {e}")
                    messages.error(request, 'Error sending email notification.')
                    
            # Check if the event date is today
            event_date = form.cleaned_data.get('event_date')
            if event_date == now().date():
                try:
                    # Send email notification for event reminder
                    send_event_reminder_email(request.user.email, event_date)
                except Exception as e:
                    # Log or print the exception for debugging
                    print(f"Error sending event reminder email: {e}")
                    messages.error(request, 'Error sending event reminder email.')
                    
            # Redirect to a success page or wherever appropriate
            return redirect('rm_suc')  # Update with the appropriate URL name
    else:
        form = ReminderSettingsForm(instance=reminder_settings)

    return render(request, 'remind.html', {'form': form})


@login_required
def send_event_reminder_email(recipient_email, event_date):
    subject = 'Event Reminder'
    message = render_to_string('event_reminder.html', {'event_date': event_date})
    sender_email = 'enote7y@gmail.com'  # Update with your sender email
    send_mail(subject, message, sender_email, [recipient_email])


#notifying
from django.conf import settings
from django.template.loader import render_to_string

@login_required
def reminder_settings_updated(request):
    # Retrieve the user and their updated reminder settings
    user = request.user
    reminder_settings = user.remindersettings

    # Render the email content template with appropriate context
    email_subject = 'Reminder Settings Updated'

    # Include the event date in the email template context
    event_date = reminder_settings.event_date.strftime('%Y-%m-%d') if reminder_settings.event_date else None

    email_body = render_to_string('reminder_settings_updated.html', {
        'user': user,
        'domain': settings.DOMAIN,  # Your website domain
        'settings_url': 'URL to view the reminder settings',  # Update with the actual URL
        'event_date': event_date,  # Pass the event date to the template context
    })

    # Send the email
    send_mail(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,  # Sender's email address
        [user.email],  # Recipient's email address (can be a list for multiple recipients)
        fail_silently=False,  # Set to True to suppress errors
    )

    # Optionally, you can render a template to confirm to the user that the email has been sent
    return render(request, 'email_sent_confirmation.html')

@login_required
def email_sent_confirmation(request):
    return render(request, 'email_sent_confirmation.html')

@login_required
def event_reminder(request):
    event_date = request.POST.get('event_date')  # Assuming event_date is passed in the POST request
    username = request.POST.get('username')  # Assuming event_date is passed in the POST request
    message = f"{username}, This is a reminder for the upcoming Child immunization set on {event_date}. Please make sure to attend and complete necessary preparations. Thank you!"
    context = {
        'message': message
    }
    return render(request, 'event_reminder.html', context)
