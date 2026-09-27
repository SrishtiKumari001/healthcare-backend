from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)
    doctor_count = serializers.IntegerField(source="doctor_mappings.count", read_only=True)

    class Meta:
        model = Patient
        fields = (
            "id", "name", "age", "gender", "contact_number", "address",
            "blood_group", "diagnosis", "admitted",
            "created_by", "created_by_name", "doctor_count",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate_contact_number(self, value):
        digits = value.replace("+", "").replace(" ", "").replace("-", "")
        if not digits.isdigit() or len(digits) < 7:
            raise serializers.ValidationError("Enter a valid contact number.")
        return value

    def validate_age(self, value):
        if value < 0 or value > 130:
            raise serializers.ValidationError("Age must be realistic (0-130).")
        return value
