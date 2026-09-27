from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """
    /api/doctors/            GET (list all), POST (create - auth required)
    /api/doctors/<id>/       GET, PUT, PATCH, DELETE
    """
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "specialization", "hospital_name"]
    ordering_fields = ["created_at", "experience_years", "name"]

    def get_queryset(self):
        return Doctor.objects.all().select_related("created_by")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "message": "Doctor added successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {"success": True, "message": "Doctors retrieved.", "data": response.data}
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {"success": True, "message": "Doctor updated.", "data": response.data}
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"success": True, "message": "Doctor record deleted."}, status=status.HTTP_200_OK)
