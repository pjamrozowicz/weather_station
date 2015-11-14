from django.db import models

# Create your models here.
class Temperature(models.Model):
    temperature = models.FloatField(editable=False)
    correctness = models.BooleanField()
    description = models.CharField(max_length=255)
    measured = models.DateTimeField(auto_now_add=True, editable=False)


class Newsletter(models.Model):
    name = models.CharField(max_length=120, blank=False)
    email = models.EmailField()

    def __str__(self):
        return self.email