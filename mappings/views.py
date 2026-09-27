from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """
    /api/mappings/                     GET (list), POST (assign doctor to patient)
    /api/mappings/<id>/                DELETE (remove mapping)
    /api/mappings/<patient_id>/        GET (custom action: all doctors for a patient)
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            created_by=self.request.user
        ).select_related("patient", "doctor")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "message": "Doctor assigned to patient.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"success": True, "message": "Mappings retrieved.", "data": response.data})

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"success": True, "message": "Mapping removed."}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/mappings/<patient_id>/ — per the spec, this endpoint returns
        every doctor assigned to a specific patient (not a single mapping row).
        """
        patient_id = kwargs.get("pk")
        patient = get_object_or_404(Patient, pk=patient_id, created_by=request.user)
        mappings = self.get_queryset().filter(patient=patient)
        serializer = self.get_serializer(mappings, many=True)
        return Response(
            {
                "success": True,
                "message": f"Doctors assigned to {patient.name}.",
                "data": serializer.data,
            }
        )
