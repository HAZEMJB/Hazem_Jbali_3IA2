from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
#from ConferenceApp.models import Conference  //Methode2

# Create your models here.

def validate_session_times(start_time, end_time):
    """Vérifie que l'heure de fin est supérieure à l'heure de début."""
    if end_time <= start_time:
        raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")


class Session(models.Model):
    Session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_validator = RegexValidator(
        regex=r'^[A-Za-z0-9\s-]+$',
        message='Le nom de la salle doit contenir uniquement des lettres, des chiffres, des espaces et des tirets.'
    )
    room = models.CharField(max_length=255,validators=[room_validator])
    created_at = models.DateTimeField(auto_now_add=True) #juste une seule fois
    updated_at = models.DateTimeField(auto_now=True) #chaque update
    conference = models.ForeignKey('ConferenceApp.Conference', on_delete=models.CASCADE, related_name='sessions')
    #conference = models.ForeignKey('Conference', on_delete=models.CASCADE, related_name='sessions') //Methode2
    def clean(self):
        if self.end_time and self.start_time:
            validate_session_times(self.start_time, self.end_time)

        if self.conference and self.session_day:
            if not self.conference.start_date  <= self.session_day <= self.conference.end_date:
                raise ValidationError("La date de la session doit être comprise entre la date de début et la date de fin de la conférence.")



