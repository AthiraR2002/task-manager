from django.contrib import admin
from .models import Profile, Job, JobApplication, Message
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister the default User model so we can redefine it with profile fields
admin.site.unregister(User)

# Inline class to display Profile fields directly on the User edit page
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Alumni/Student Details'
    # Display the custom fields for editing
    fields = ('is_alumni', 'batch_year_range', 'department', 'bio')


# Custom UserAdmin to integrate the Profile model
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
    # Customize the user list view for quick user management (Data Integrity)
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'is_active',
        'is_alumni_display' # Custom method to display alumni status
    )
    
    # Add a filter option for alumni status
    list_filter = ('is_staff', 'is_active', 'profile__is_alumni')

    # Method to display the 'is_alumni' status from the related Profile object
    def is_alumni_display(self, obj):
        return obj.profile.is_alumni if hasattr(obj, 'profile') else False
    is_alumni_display.boolean = True
    is_alumni_display.short_description = 'Is Alumni'


# ---------------------------------------------------------------------

# 1. Moderation and Reporting for Jobs
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # This displays key metrics for Engagement Reporting
    list_display = ('title', 'company', 'posted_by', 'posted_date')
    list_filter = ('posted_date', 'company')
    search_fields = ('title', 'description', 'company')
    # Fields to allow the admin to manage content
    fields = ('title', 'company', 'location', 'description', 'posted_by')
    
# 2. Moderation and Reporting for Applications
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    # Displays all necessary application details
    list_display = ('job', 'applicant', 'applied_date')
    list_filter = ('job__company', 'applied_date')
    search_fields = ('applicant__username', 'cover_letter')
    # Make job and applicant read-only to prevent tampering
    readonly_fields = ('job', 'applicant', 'applied_date')

# 3. Moderation and Reporting for Messages
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Displays details needed for content moderation/reporting
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'body')
    # Ensure messages cannot be edited after creation
    readonly_fields = ('sender', 'receiver', 'body', 'timestamp')
