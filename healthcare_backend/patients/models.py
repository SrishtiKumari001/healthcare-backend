from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Patient(models.Model):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female"), ("other", "Other")]
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-"), ("unknown", "Unknown"),
    ]

    name = models.CharField(max_length=150)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(130)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default="unknown")
    diagnosis = models.CharField(max_length=255, blank=True, help_text="Current diagnosis / condition")
    admitted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patients"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.age}, {self.gender})"
