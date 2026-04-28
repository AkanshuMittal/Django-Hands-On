"""
========================================================
  accounts/models.py
  STEP 2: Custom User Model
========================================================

WHY CUSTOM USER MODEL?
  Django's default User model only has: username, email, password, first_name, last_name.
  We need a 'role' field to distinguish Employers from Candidates.

  GOLDEN RULE: Always create a custom user model BEFORE your first migration.
  Changing it later is painful and messy. Every real company does this.

  We use AbstractBaseUser + PermissionsMixin — this gives us full control
  while keeping Django's built-in auth system (login, permissions, admin) working.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# ─── CUSTOM USER MANAGER ──────────────────────────────────────────────────────
# WHY: When you use AbstractBaseUser, Django doesn't know HOW to create users.
#      You must tell it by writing a custom Manager.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Called when: User.objects.create_user(email='...', password='...')
        This is what your registration view will use.
        """
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)  # lowercase the domain part
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes the password (never store plain text)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Called when: python manage.py createsuperuser
        Superuser = Django admin access
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# ─── CUSTOM USER MODEL ────────────────────────────────────────────────────────
class User(AbstractBaseUser, PermissionsMixin):
    """
    Our main User model. Replaces Django's default User.

    LOGIN WITH EMAIL (not username):
      In real companies, users log in with email. Much better UX.
      We set USERNAME_FIELD = 'email' to achieve this.
    """

    # Role choices — company has 2 types of users
    EMPLOYER = 'employer'
    CANDIDATE = 'candidate'
    ROLE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (CANDIDATE, 'Candidate'),
    ]

    # ── Core fields ────────────────────────────────────────────────────────
    email      = models.EmailField(unique=True)               # Used as login username
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CANDIDATE)

    # ── Profile fields ─────────────────────────────────────────────────────
    phone      = models.CharField(max_length=15, blank=True)
    bio        = models.TextField(blank=True)
    # Candidate: uploads their profile photo
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    # ── Django admin/auth required fields ──────────────────────────────────
    is_active  = models.BooleanField(default=True)   # Can this user log in?
    is_staff   = models.BooleanField(default=False)  # Can access /admin/?
    date_joined = models.DateTimeField(auto_now_add=True)

    # ── Tell Django to use our custom manager ──────────────────────────────
    objects = UserManager()

    # ── Use EMAIL as the login identifier (not username) ───────────────────
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']  # required for createsuperuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Helper properties — use these in templates and views
    @property
    def is_employer(self):
        return self.role == self.EMPLOYER

    @property
    def is_candidate(self):
        return self.role == self.CANDIDATE


# ─── EMPLOYER PROFILE ─────────────────────────────────────────────────────────
# WHY SEPARATE MODEL: Employers have company-specific data.
#     Keeping it separate keeps User model clean.
#     This is called a "OneToOne extension" — a common pattern in real projects.
class EmployerProfile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=100)
    company_website = models.URLField(blank=True)
    company_size = models.CharField(max_length=50, blank=True,
                                    help_text="e.g. 1-10, 11-50, 51-200")
    industry     = models.CharField(max_length=100, blank=True)
    company_description = models.TextField(blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


# ─── CANDIDATE PROFILE ────────────────────────────────────────────────────────
class CandidateProfile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    resume       = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills       = models.TextField(blank=True, help_text="Comma separated: Python, Django, React")
    experience_years = models.PositiveIntegerField(default=0)
    current_job_title = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url   = models.URLField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Candidate"
    

