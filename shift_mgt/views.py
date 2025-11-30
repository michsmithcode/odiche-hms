from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Shift
from .serializers import ShiftSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def shift_list_create(request):
    # GET → List all shifts
    if request.method == "GET":
        shifts = Shift.objects.all().order_by("date", "start_time")
        serializer = ShiftSerializer(shifts, many=True)
        return Response(serializer.data)

    # POST → Create a new shift
    if request.method == "POST":
        serializer = ShiftSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()  # assigned_by auto-filled in serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def shift_detail(request, shift_id):

    try:
        shift = Shift.objects.get(id=shift_id)
    except Shift.DoesNotExist:
        return Response({"error": "Shift not found"}, status=status.HTTP_404_NOT_FOUND)

    # GET → Retrieve
    if request.method == "GET":
        serializer = ShiftSerializer(shift)
        return Response(serializer.data)

    # PUT/PATCH → Update
    if request.method in ["PUT", "PATCH"]:
        serializer = ShiftSerializer(
            shift,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE → Remove shift
    if request.method == "DELETE":
        shift.delete()
        return Response({"message": "Shift deleted successfully"}, status=status.HTTP_200_OK)
