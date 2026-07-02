from django import forms
from django.contrib.auth.forms import UserCreationForm
# Imports all necessary models and the constant
from .models import Job, JobApplication, Profile, Message
from .constants import COURSE_CHOICES 

# Define Program Choices here, as they are only used in this form/view.
# Renamed COURSE_CHOICES to DEPT_CHOICES for clarity within the form.
DEPT_CHOICES = COURSE_CHOICES

PROGRAM_CHOICES = (
    ('BT', 'B.Tech'),
    ('INMCA', 'MCA (Integrated)'), # Renamed INM for clarity
    ('MBA', 'MBA'),
    ('MCA', 'MCA (Regular)'),
)

# =================================================================
# 1. JOB FORMS
# =================================================================
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'description']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter']

# =================================================================
# 2. REGISTRATION FORMS
# =================================================================
class StudentRegistrationForm(UserCreationForm):
    pass

class AlumniRegistrationForm(UserCreationForm):
    # Field 1: Batch Year Range
    batch_year_range = forms.CharField(
        max_length=50, 
        required=True,
        help_text="e.g., 2021-2024"
    )
    
    # Field 2: Department/Discipline (Dropdown using COURSE_CHOICES/DEPT_CHOICES)
    department = forms.ChoiceField(
        choices=DEPT_CHOICES, 
        required=True,
        label="Department" # Corrected field name and label
    ) 

    # NEW COLUMN (Field 3): Course/Program Type (Dropdown using PROGRAM_CHOICES)
    course_program = forms.ChoiceField(
        choices=PROGRAM_CHOICES,
        required=True,
        label="Course/Program Name"
    )

    class Meta(UserCreationForm.Meta):
        pass

    # The save and init methods are now CORRECTLY inside the class
    def save(self, commit=True):
        user = super().save(commit=True)
        if commit:
            Profile.objects.create(
                user=user, 
                is_alumni=True,
                # CRITICAL: Save the three custom fields
                batch_year_range=self.cleaned_data['batch_year_range'],
                department=self.cleaned_data['department'], 
                course_program=self.cleaned_data['course_program'], 
            )
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Please enter a unique username."


# =================================================================
# 3. MESSAGE FORM
# =================================================================
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }