from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import LabTest, LabTestResult
from .serializers import LabTestSerializer, LabTestResultSerializer


#Request for labtest by Doctor
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_lab_test(request):
    serializer = LabTestSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(
            ordered_by=request.user.doctor_profile
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_lab_tests(request):
    tests = LabTest.objects.filter(status="pending")
    serializer = LabTestSerializer(tests, many=True)
    return Response(serializer.data)


#Uploading lab result

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_lab_result(request, test_id):
    try:
        lab_test = LabTest.objects.get(id=test_id)
    except LabTest.DoesNotExist:
        return Response(
            {"error": "Lab test not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if hasattr(lab_test, "result"):
        return Response(
            {"error": "Result already uploaded"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = LabTestResultSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(
            lab_test=lab_test,
            technician=request.user.labtechnician_profile
        )
        lab_test.status = "completed"
        lab_test.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Preventing unatutorized acccess to lab result except Admin/doctor
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_lab_result(request, result_id):
    try:
        result = LabTestResult.objects.get(id=result_id)
    except LabTestResult.DoesNotExist:
        return Response(
            {"error": "Result not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    result.is_verified = True
    result.save()

    return Response({"message": "Lab result verified successfully"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def patient_lab_results(request, patient_id):
    tests = LabTest.objects.filter(patient_id=patient_id, status="completed")
    serializer = LabTestSerializer(tests, many=True)
    return Response(serializer.data)


