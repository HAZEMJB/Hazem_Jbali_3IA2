from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
import uuid


def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()

def validate_university_email(email):
    domaine=["esprit.tn","seasame.tn","ihec.tn","supcom.tn","tek.tn","central.tn"]
    email_domain = email.split('@')[1]
    if email_domain not in domaine:
        raise ValidationError("Email est invalide il doit appartenir a une universite")

name_validators = RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message='Le nom doit contenir uniquement des lettres alphabétiques et des epaces .'
)

class User(AbstractUser):
    user_id = models.CharField(max_length=8, unique=True,primary_key=True,editable=False)
    first_name = models.CharField(max_length=30,validators=[name_validators])
    last_name = models.CharField(max_length=30,validators=[name_validators])
    affiliation = models.CharField(max_length=100)
    ROLE=[
        ('participant', 'participant'),
        ('commitee', 'organizing commitee member'),
    ]
    role = models.CharField(max_length=20, choices=ROLE, default='participant')
    email = models.EmailField(unique=True,validators=[validate_university_email])
    nationality = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) #juste une seule fois
    updated_at = models.DateTimeField(auto_now=True) #chaque update
    def save(self, *args, **kwargs):
        if not self.user_id:
            new_id = generate_user_id()
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_user_id()
            self.user_id = new_id
        super().save(*args, **kwargs)

class Organizing_committee_member(models.Model):
    ROLE=[
        ('chair', 'Chair'),
        ('co-chair', 'Co-Chair'),
        ('member', 'Member'),
    ]
    commitee_role = models.CharField(max_length=255,choices=ROLE)
    date_joined = models.DateField()
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='committee_member')
    conference = models.ForeignKey('ConferenceApp.Conference', on_delete=models.CASCADE, related_name='committee_members')
    created_at = models.DateTimeField(auto_now_add=True) #juste une seule fois
    updated_at = models.DateTimeField(auto_now=True) #chaque update