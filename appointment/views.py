from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from doctors.models import DoctorProfile
from patients.models import PatientProfile
from nurses.models import NurseProfile



#auto assign
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppointmentSerializer
from .models import Appointment
from nurses.utils import get_available_nurse_for_datetime
from doctors.utils import assign_doctor_by_specialization
from notifications.utils import send_appointment_notification


@api_view(["POST"])
@permission_classes([])
def create_appointment(request):
    serializer = AppointmentSerializer(data=request.data)

    if serializer.is_valid():

        appointment_date = serializer.validated_data["appointment_date"]
        specialization = serializer.validated_data.get("specialization")

        # Auto-assign nurse
        nurse = get_available_nurse_for_datetime(appointment_date)

        # Auto-assign doctor
        doctor = assign_doctor_by_specialization(specialization)

        if not doctor:
            return Response(
                {"error": "No doctor available for this specialization"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not nurse:
            return Response(
                {"error": "No nurse available at this time"},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment = serializer.save(
            doctor=doctor,
            nurse=nurse
        )

        # Send notifications to doctor + nurse + patient
        send_appointment_notification(appointment)

        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def perform_create(self, serializer):
    nurse = serializer.validated_data.get("nurse")
    appointment_date = serializer.validated_data["appointment_date"]

    if nurse is None:
        nurse = get_available_nurse_for_datetime(appointment_date)
        if nurse is None:
            raise ValidationError("No nurse available.")

    serializer.save(nurse=nurse)




# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Appointment
# from .serializers import AppointmentSerializer
# from shift_mgt.shift_assignment import get_available_nurse_for_datetime   # your auto-assignment function


# # ==========================================
# # LIST + CREATE APPOINTMENTS
# # ==========================================
# @api_view(["GET", "POST"])
# def appointment_list_create(request):
#     # =============================
#     # GET → List All Appointments
#     # =============================
#     if request.method == "GET":
#         appointments = Appointment.objects.all()
#         serializer = AppointmentSerializer(appointments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     # =============================
#     # POST → Create Appointment
#     # =============================
#     if request.method == "POST":
#         serializer = AppointmentSerializer(data=request.data)

#         if serializer.is_valid():
#             appointment_date = serializer.validated_data["appointment_date"]

#             # Auto-assign nurse
#             nurse = get_available_nurse_for_datetime(appointment_date)

#             if nurse is None:
#                 return Response(
#                     {"error": "No nurse is available during this time slot."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             serializer.save(nurse=nurse)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ===================================
# List all appointments (Admin or Staff)
# ===================================
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_appointments(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# ===================================
# Retrieve single appointment
# ===================================
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def appointment_detail(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data)


# ===================================
# Create new appointment
# ===================================
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_appointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===================================
# Update appointment (PATCH only)
# ===================================
@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===================================
# Delete appointment by admin permission
# ===================================
@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])  
def delete_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    appointment.delete()
    return Response({"message": "Appointment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
