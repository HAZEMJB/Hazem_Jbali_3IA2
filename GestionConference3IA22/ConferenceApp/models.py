from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.
def validate_keywords(keywords):
    keywords=[keyword.strip() for keyword in keywords.split(',')]
    if len(keywords)>10:
        raise ValidationError("Vous ne pouvez pas entrer plus de 10 mots-clés.")
    
def generate_submission_id():
    import uuid
    return "SUB-"+uuid.uuid4().hex[:8].upper()

class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s-]+$',
                message='Le nom doit contenir uniquement des lettres alphabétiques et des epaces .'
            )
        ]
    )
    THEME =[
        ('CS', 'Computer Science'),
        ('AI', 'Artificial Intelligence'),
        ('SE', 'Science & Engineering'),
        ('SSE', 'Social Sciences & Education'),
        ('IT', 'Interdisciplinary Themes'),
    ]
    theme = models.CharField(max_length=255,choices=THEME)
    #theme = models.CharField(max_length=255,choices=['CS', 'AI', 'SE', 'SSE', 'IT'])
    location = models.CharField(max_length=255)
    description = models.TextField(validators=[MinLengthValidator(30,"Minimum 30 characters.")]) 
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True) #juste une seule fois
    updated_at = models.DateTimeField(auto_now=True) #chaque update
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")


class Submission(models.Model):
    Submission_id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False
    )
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keyword = models.TextField(validators=[validate_keywords])
    paper = models.FileField(
        upload_to='papers/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    STATUS = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='submitted')
    submission_date = models.DateTimeField(default=timezone.now)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='submissions')
    conference = models.ForeignKey('Conference', on_delete=models.CASCADE, related_name='submissions')

    def clean(self):
        today = timezone.now().date()

        # Conférences à venir uniquement
        if self.conference.start_date <= today:
            raise ValidationError("❌ La soumission ne peut être faite que pour des conférences à venir.")

        # Limite de 3 soumissions par jour
        count_today = Submission.objects.filter(
            user=self.user,
            submission_date__date=today
        ).exclude(pk=self.pk).count()

        if count_today >= 3:
            raise ValidationError("⚠️ Vous ne pouvez pas soumettre à plus de 3 conférences par jour.")

    def save(self, *args, **kwargs):
        # 🔹 Génère un ID unique si inexistant
        if not self.Submission_id:
            self.Submission_id = generate_submission_id()

        # 🔹 Valide avant sauvegarde
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.user}"



