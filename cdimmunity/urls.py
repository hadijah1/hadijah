from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('remind/', remind, name='remind'),
    path('rm_suc/', rm_suc, name='rm_suc'),
    path('cldreg/', cldreg, name='cldreg'),
    path('event_reminder/', event_reminder, name='event_reminder'),
    path('reminder-settings-updated/', reminder_settings_updated, name='reminder_settings_updated'),
    path('email_sent_confirmation/', email_sent_confirmation, name='email_sent_confirmation'),
    path('cldreg_success/', cldreg_success, name='cldreg_success'),
    path('immunization_schedule/', immunization_schedule, name='immunization_schedule'),
    path('view_schedule/', view_schedule, name='view_schedule'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
]
