from django.db import models

class CV(models.Model):
    firstname  = models.CharField(max_length=50)
    lastname   = models.CharField(max_length=50)
    skills     = models.TextField(blank=True)
    projects   = models.TextField(blank=True)
    bio        = models.TextField(blank=True)
    contacts   = models.TextField(blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

