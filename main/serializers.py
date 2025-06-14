from rest_framework import serializers
from .models import CV

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ["id", "firstname", "lastname", "skills", "projects", "bio", "contacts"]
