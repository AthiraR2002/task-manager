from django.db import models
from django.contrib.auth.models import User
from .constants import COURSE_CHOICES 

# Define new choices for the Degree Program (must match what's in forms.py)
PROGRAM_CHOICES = (
    ('BT', 'B.Tech'),
    ('INMCA', 'MCA (Integrated)'),
    ('MBA', 'MBA'),
    ('MCA', 'MCA (Regular)'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_alumni = models.BooleanField(default=False)
    
    # Custom Field 1: Batch Year Range
    batch_year_range = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="e.g., 2021-2024"
    )

    # Field 2: Department/Discipline
    department = models.CharField(
        max_length=50, 
        choices=COURSE_CHOICES, 
        blank=True, 
        null=True
    )
    
    # NEW FIELD 3: Degree Program/Course Name
    course_program = models.CharField(
        max_length=50, 
        choices=PROGRAM_CHOICES, # Uses the new choices defined above
        blank=True, 
        null=True
    )
    
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile ({'Alumni' if self.is_alumni else 'Student'})"

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField()
    applied_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"