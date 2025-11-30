# from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from doctors.models import Doctor
from nurses.models import NurseProfile
from pharmarcist.models import PharmacistProfile
from patients.models import Patient
from pharmacy_cashier.models import PharmacyCashier  # if exists

from doctors.serializers import DoctorProfileSerializer
from nurses.serializers import NurseSerializer
from pharmacist.serializers import PharmacistSerializer
from patients.serializers import PatientSerializer
from pharmacy_cashier.serializers import PharmacyCashierSerializer

#Admin dashboardoverview
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from doctor.models import Doctor
from nurse.models import Nurse
from pharmacist.models import Pharmacist
from pharmacy_cashier.models import PharmacyCashier
from patient.models import Patient
from appointment.models import Appointment  # Uncomment if available
from payments.models import Payment  # Uncomment if available
from permissions.decorators import permission_required


#admin access control

@permission_required("can_manage_permissions")
def admin_manage_roles(request):
    return Response({"message": "Main Admin managing roles"})



@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_dashboard_overview(request):
    """
    GET /api/admin/dashboard/
    Returns counts and statistics for all hospital users and optionally appointments/payments.
    """
    try:
        total_doctors = Doctor.objects.count()
        total_nurses = Nurse.objects.count()
        total_pharmacists = Pharmacist.objects.count()
        total_cashiers = PharmacyCashier.objects.count()
        total_patients = Patient.objects.count()

        # Example if you have appointments
        # total_appointments = Appointment.objects.count()
        # pending_appointments = Appointment.objects.filter(status="pending").count()
        # completed_appointments = Appointment.objects.filter(status="completed").count()

        # Example if you have a payment model
        # total_revenue = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0

        dashboard_data = {
            "users_summary": {
                "doctors": total_doctors,
                "nurses": total_nurses,
                "pharmacists": total_pharmacists,
                "cashiers": total_cashiers,
                "patients": total_patients,
            },
            # Uncomment when ready
            # "appointments": {
            #     "total": total_appointments,
            #     "pending": pending_appointments,
            #     "completed": completed_appointments,
            # },
            # "finance": {
            #     "total_revenue": total_revenue,
            # },
        }

        return Response(dashboard_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Something went wrong: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )





# ---------------------------
# DOCTOR MANAGEMENT
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_doctors(request):
    doctors = Doctor.objects.all().select_related("user")
    serializer = DoctorProfileSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAdminUser])
def admin_doctor_detail(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DoctorProfileSerializer(doctor)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        doctor.delete()
        return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ---------------------------
# NURSE MANAGEMENT
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_nurses(request):
    nurses = Nurse.objects.all().select_related("user")
    serializer = NurseSerializer(nurses, many=True)
    return Response(serializer.data)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAdminUser])
def admin_nurse_detail(request, nurse_id):
    try:
        nurse = Nurse.objects.get(id=nurse_id)
    except Nurse.DoesNotExist:
        return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = NurseSerializer(nurse)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = NurseSerializer(nurse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        nurse.delete()
        return Response({"message": "Nurse deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ---------------------------
# PHARMACIST MANAGEMENT
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_pharmacists(request):
    pharmacists = Pharmacist.objects.all().select_related("user")
    serializer = PharmacistSerializer(pharmacists, many=True)
    return Response(serializer.data)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAdminUser])
def admin_pharmacist_detail(request, pharmacist_id):
    try:
        pharmacist = Pharmacist.objects.get(id=pharmacist_id)
    except Pharmacist.DoesNotExist:
        return Response({"error": "Pharmacist not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PharmacistSerializer(pharmacist)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = PharmacistSerializer(pharmacist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        pharmacist.delete()
        return Response({"message": "Pharmacist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ---------------------------
# PHARMACY CASHIER MANAGEMENT
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_cashiers(request):
    cashiers = PharmacyCashier.objects.all().select_related("user")
    serializer = PharmacyCashierSerializer(cashiers, many=True)
    return Response(serializer.data)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAdminUser])
def admin_cashier_detail(request, cashier_id):
    try:
        cashier = PharmacyCashier.objects.get(id=cashier_id)
    except PharmacyCashier.DoesNotExist:
        return Response({"error": "Cashier not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PharmacyCashierSerializer(cashier)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = PharmacyCashierSerializer(cashier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        cashier.delete()
        return Response({"message": "Cashier deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ---------------------------
# PATIENT MANAGEMENT
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_patients(request):
    patients = Patient.objects.all().select_related("user")
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAdminUser])
def admin_patient_detail(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        patient.delete()
        return Response({"message": "Patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework import status
# from doctors.models import Doctor
# from doctors.serializers import DoctorProfileSerializer


# @api_view(["GET"])
# @permission_classes([IsAdminUser])
# def admin_list_doctors(request):
#     """
#     GET /admin/doctors/ - List all doctor profiles (Admin only)
#     """
#     doctors = Doctor.objects.all().select_related("user")
#     serializer = DoctorProfileSerializer(doctors, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["GET"])
# @permission_classes([IsAdminUser])
# def admin_get_doctor(request, doctor_id):
#     """
#     GET /admin/doctors/<id>/ - Retrieve specific doctor profile (Admin only)
#     """
#     try:
#         doctor = Doctor.objects.get(id=doctor_id)
#     except Doctor.DoesNotExist:
#         return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
#     serializer = DoctorProfileSerializer(doctor)
#     return Response(serializer.data)


# @api_view(["PATCH"])
# @permission_classes([IsAdminUser])
# def admin_update_doctor(request, doctor_id):
#     """
#     PATCH /admin/doctors/<id>/update/ - Update doctor profile (Admin only)
#     """
#     try:
#         doctor = Doctor.objects.get(id=doctor_id)
#     except Doctor.DoesNotExist:
#         return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

#     serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["DELETE"])
# @permission_classes([IsAdminUser])
# def admin_delete_doctor(request, doctor_id):
#     """
#     DELETE /admin/doctors/<id>/delete/ - Delete doctor profile (Admin only)
#     """
#     try:
#         doctor = Doctor.objects.get(id=doctor_id)
#         doctor.delete()
#         return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#     except Doctor.DoesNotExist:
#         return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
