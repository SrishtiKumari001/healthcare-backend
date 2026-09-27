from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)
    doctor_specialization = serializers.CharField(source="doctor.specialization", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = (
            "id", "patient", "patient_name", "doctor", "doctor_name",
            "doctor_specialization", "notes", "assigned_date", "created_by",
        )
        read_only_fields = ("id", "assigned_date", "created_by")

    def validate(self, attrs):
        patient = attrs.get("patient") or getattr(self.instance, "patient", None)
        doctor = attrs.get("doctor") or getattr(self.instance, "doctor", None)

        request = self.context["request"]
        if patient and patient.created_by_id != request.user.id:
            raise serializers.ValidationError("You can only map patients you created.")

        if patient and doctor:
            qs = PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return attrs
