from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)
    specialization_display = serializers.CharField(source="get_specialization_display", read_only=True)
    patient_count = serializers.IntegerField(source="patient_mappings.count", read_only=True)

    class Meta:
        model = Doctor
        fields = (
            "id", "name", "specialization", "specialization_display", "email",
            "phone_number", "experience_years", "hospital_name",
            "created_by", "created_by_name", "patient_count",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate_phone_number(self, value):
        digits = value.replace("+", "").replace(" ", "").replace("-", "")
        if not digits.isdigit() or len(digits) < 7:
            raise serializers.ValidationError("Enter a valid phone number.")
        return value

    def validate_experience_years(self, value):
        if value < 0 or value > 70:
            raise serializers.ValidationError("Experience years must be between 0 and 70.")
        return value
