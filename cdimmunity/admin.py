from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.safestring import mark_safe

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_superuser')  # Include 'is_staff' and 'is_superuser'
    search_fields = ('email', 'username')
    readonly_fields = ('last_login',)  # Remove 'date_joined'

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Profile Picture', {'fields': ('profile_picture',)}),  # Add this line for profile picture
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser', 'profile_picture')}  # Include profile_picture in add fieldsets
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)


# Register the Child model
@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'child_name', 'child_date_of_birth']
    search_fields = ['email', 'first_name', 'last_name', 'child_name']
    list_filter = ['child_gender', 'child_blood_type']


#immune schedule
@admin.register(ImmunizationSchedule)
class ImmunizationScheduleAdmin(admin.ModelAdmin):
    list_display = ['vaccine_name', 'child_name', 'recommended_age', 'number_of_doses', 'additional_info', 'child_image_thumbnail']
    search_fields = ['vaccine_name', 'child_name']
    list_filter = ['recommended_age']

    def child_image_thumbnail(self, obj):
        if obj.child_image:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.child_image.url,
                width=obj.child_image.width,
                height=obj.child_image.height,
            ))
        else:
            return 'No Image'
    child_image_thumbnail.short_description = 'Child Image'

#R  eminder
@admin.register(ReminderSettings)
class ReminderSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_reminder', 'sms_reminder']
    list_filter = ['email_reminder', 'sms_reminder']
    search_fields = ['user__username', 'user__email']