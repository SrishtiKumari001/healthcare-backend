from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Patient
from .serializers import PatientSerializer


class IsOwner(permissions.BasePermission):
    """Only the user who created a patient record may view/modify it."""
    def has_object_permission(self, request, view, obj):
        return obj.created_by_id == request.user.id


class PatientViewSet(viewsets.ModelViewSet):
    """
    /api/patients/            GET (own patients), POST (create - auth required)
    /api/patients/<id>/       GET, PUT, PATCH, DELETE (owner only)
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    search_fields = ["name", "diagnosis", "blood_group"]
    ordering_fields = ["created_at", "age", "name"]

    def get_queryset(self):
        # Spec: "Retrieve all patients created by the authenticated user"
        return Patient.objects.filter(created_by=self.request.user).select_related("created_by")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.created_by_id != self.request.user.id:
            raise PermissionDenied("You can only update patients you created.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.created_by_id != self.request.user.id:
            raise PermissionDenied("You can only delete patients you created.")
        instance.delete()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "message": "Patient added successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"success": True, "message": "Patients retrieved.", "data": response.data})

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {"success": True, "message": "Patient updated.", "data": response.data}
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"success": True, "message": "Patient record deleted."}, status=status.HTTP_200_OK)
