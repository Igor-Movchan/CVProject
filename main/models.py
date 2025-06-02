from django.db import models
from django.conf import settings

class CV(models.Model):
    firstname  = models.CharField(max_length=50)
    lastname   = models.CharField(max_length=50)
    skills     = models.TextField(blank=True)
    projects   = models.TextField(blank=True)
    bio        = models.TextField(blank=True)
    contacts   = models.TextField(blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class RequestLog(models.Model):
    timestamp    = models.DateTimeField(auto_now_add=True)
    method       = models.CharField(max_length=10)
    path         = models.CharField(max_length=200)
    query_string = models.CharField(max_length=500, blank=True)
    remote_ip    = models.CharField(max_length=45, blank=True)
    user         = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"[{self.timestamp}] {self.method} {self.path}"

