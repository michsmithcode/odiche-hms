from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from patients.models import PatientProfile
from django.db.models import Q
from django.utils.timezone import localtime

from datetime import time


"""
testing
 "paitient": "patient-reg_no-REG/2025/24332",
    "appointment_date": "2025-12-15T10:30",
    appointment_time
"""


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    """
    Doctor books appointment for a patient.
    Uses doctor's shift (single-day: date, start_time, end_time).
    """

    # Ensure logged-in user is a doctor
    doctor = getattr(request.user, "doctor_profile", None)
    if not doctor:
        return Response({"error": "Only doctors can create appointments."}, status=403)

    # Validate data
    serializer = AppointmentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    patient = serializer.validated_data["patient"]
    appointment_date = serializer.validated_data["appointment_date"]

    # Convert to local timezone
    local_appt = localtime(appointment_date)
    appt_day = local_appt.date()
    appt_time = local_appt.time()

    # Import Shift dynamically
    from shift_mgt.models import Shift

    # Find shifts assigned to this doctor on this date
    doctor_shifts = Shift.objects.filter(
        user=doctor.user,
        date=appt_day
    )

    if not doctor_shifts.exists():
        return Response({"error": "You have no shift assigned."}, status=400)
    #shift = doctor_shifts.first()

    # Find shift that matches the time
    matching_shift = doctor_shifts.filter(
        start_time__lte=appt_time,
        end_time__gte=appt_time
    ).first()

    if not matching_shift:
        return Response(
            {"error": "Doctor is not available during this time."},
            status=400
        )

    # Prevent double booking
    if Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date
    ).exists():
        return Response(
            {"error": "You already have an appointment at this time."},
            status=400
        )

    # Create appointment
    appointment = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        appointment_date=appointment_date
    )

    return Response(
        {
            "message": "Appointment created successfully",
            "appointment": AppointmentSerializer(appointment).data
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def doctor_view_appointments(request):
    doctor = getattr(request.user, "doctor_profile", None)

    if not doctor:
        return Response({"error": "Only doctors can view this."}, status=403)

    appointments = Appointment.objects.filter(doctor=doctor).order_by("appointment_date")

    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def doctor_search_patients(request):
    keyword = request.GET.get("q", "")

    patients = PatientProfile.objects.filter(
        Q(user__first_name__icontains=keyword) |
        Q(user__last_name__icontains=keyword) |
        Q(reg_no__icontains=keyword)
    )

    data = [
        {
            "id": p.id,
            "name": f"{p.user.first_name} {p.user.last_name}",
            "reg_no": p.reg_no,
        }
        for p in patients
    ]

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_appointments(request):
    appointments = Appointment.objects.all().order_by("-appointment_date")
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def appointment_detail(request, pk):
    try:
        appointment = Appointment.objects.get(id=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=404)

    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data)



@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(id=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=404)

    serializer = AppointmentSerializer(appointment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Appointment updated successfully",
            "appointment": serializer.data
        })

    return Response(serializer.errors, status=400)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_appointment_status(request, pk):
    try:
        appointment = Appointment.objects.get(id=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=404)

    new_status = request.data.get("status")

    if new_status not in ["pending", "confirmed", "completed", "cancelled"]:
        return Response({"error": "Invalid status"}, status=400)

    appointment.status = new_status
    appointment.save()

    return Response({
        "message": f"Appointment marked as {new_status}",
        "appointment": AppointmentSerializer(appointment).data
    })


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(id=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=404)

    appointment.delete()
    return Response({"message": "Appointment deleted successfully"}, status=204)

