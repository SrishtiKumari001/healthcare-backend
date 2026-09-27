from django.db import models
from django.conf import settings


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ("cardiology", "Cardiology"),
        ("dermatology", "Dermatology"),
        ("neurology", "Neurology"),
        ("orthopedics", "Orthopedics"),
        ("pediatrics", "Pediatrics"),
        ("general", "General Physician"),
        ("psychiatry", "Psychiatry"),
        ("gynecology", "Gynecology"),
        ("ent", "ENT"),
        ("dentistry", "Dentistry"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES, default="general")
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    experience_years = models.PositiveIntegerField(default=0)
    hospital_name = models.CharField(max_length=150, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctors"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Dr. {self.name} ({self.get_specialization_display()})"
