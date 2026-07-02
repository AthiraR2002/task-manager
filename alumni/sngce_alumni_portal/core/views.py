from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import (
    Job, JobApplication, Profile, Message
)
from .forms import (
    JobForm, JobApplicationForm, StudentRegistrationForm, 
    AlumniRegistrationForm, MessageForm
)
def alumni_list(request):
    """Displays a list of all registered alumni."""
    # Find all Users who have a profile and are marked as alumni
    alumni_users = User.objects.filter(profile__is_alumni=True).order_by('username')
    
    context = {
        'alumni_users': alumni_users
    }
    return render(request, 'core/alumni_list.html', context)

@login_required
def alumni_profile(request, pk):
    """Displays the detailed profile of a single alumnus."""
    alumnus = get_object_or_404(User, pk=pk)
    
    # Ensure the user being viewed is actually an alumnus
    if not hasattr(alumnus, 'profile') or not alumnus.profile.is_alumni:
        return redirect('alumni_list') # Redirect if not a valid alumnus profile
    
    context = {
        'alumnus': alumnus,
    }
    return render(request, 'core/alumni_profile.html', context)
# Helper function to check for profile existence
def has_profile(user):
    return hasattr(user, 'profile')

# ----------------------------------------------------------------------------------------------------
# PUBLIC-FACING VIEWS
# ----------------------------------------------------------------------------------------------------
def home(request):
    """Renders the home page, redirecting staff to the dashboard."""
    # This block performs the check when a user accesses the root path (/)
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
        
    # If not staff, render the regular public home page
    return render(request, 'core/home.html')

def job_list(request):
    """Displays a list of all available jobs."""
    jobs = Job.objects.all().order_by('-posted_date')
    return render(request, 'core/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    """Displays a detailed view of a single job. Allows a student to apply."""
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    
    # Check if user is an authenticated student
    if request.user.is_authenticated and has_profile(request.user) and not request.user.profile.is_alumni:
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobApplicationForm()
        
    context = {
        'job': job,
        'form': form,
        'has_applied': has_applied,
    }
    return render(request, 'core/job_detail.html', context)

# ----------------------------------------------------------------------------------------------------
# AUTHENTICATION & REGISTRATION VIEWS
# ----------------------------------------------------------------------------------------------------
def register_student(request):
    """Handles student registration."""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, is_alumni=False)
            return redirect('login')
        else:
            # Renders form with errors
            return render(request, 'core/register.html', {'form': form, 'user_type': 'Student'})
    else:
        form = StudentRegistrationForm()
    return render(request, 'core/register.html', {'form': form, 'user_type': 'Student'})

def register_alumni(request):
    """Handles alumni registration."""
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # The form's save method handles Profile creation for alumni
            return redirect('login')
        else:
            # Renders form with errors
            return render(request, 'core/register.html', {'form': form, 'user_type': 'Alumni'})
    else:
        form = AlumniRegistrationForm()
    return render(request, 'core/register.html', {'form': form, 'user_type': 'Alumni'})

# ----------------------------------------------------------------------------------------------------
# ALUMNI-ONLY & MESSAGING VIEWS
# ----------------------------------------------------------------------------------------------------
@login_required
def job_post(request):
    """Allows an alumni to post a new job."""
    if not has_profile(request.user) or not request.user.profile.is_alumni:
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')
        else:
            return render(request, 'core/job_post.html', {'form': form})
    else:
        form = JobForm()
    
    return render(request, 'core/job_post.html', {'form': form})

@login_required
def inbox(request):
    """Displays a list of all conversations for the logged-in user."""
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')
    
    unique_users = set()
    latest_messages = []
    
    # Logic to ensure only the latest message per conversation is shown
    for message in conversations:
        other_user = message.sender if message.sender != request.user else message.receiver
        if other_user not in unique_users:
            unique_users.add(other_user)
            latest_messages.append(message)
            
    context = {'latest_messages': latest_messages}
    return render(request, 'core/inbox.html', context)

@login_required
def compose_message(request, user_id):
    """Allows a user to compose a new message to a specific user."""
    receiver = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    
    context = {'form': form, 'receiver': receiver}
    return render(request, 'core/compose_message.html', context)

############
# In core/views.py

# Add this view function near the 'home' view
@login_required
def admin_dashboard(request):
    """
    Dedicated dashboard for logged-in staff/admin users.
    """
    if not request.user.is_staff:
        return redirect('home')
        
    alumni_count = User.objects.filter(profile__is_alumni=True).count()
    job_count = Job.objects.count()
    
    context = {
        'alumni_count': alumni_count,
        'job_count': job_count,
    }
    return render(request, 'core/admin_dashboard.html', context)