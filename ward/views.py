from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Ward, Bed
from .serializers import WardSerializer, BedSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def ward_list_create(request):
    """
    List all wards or create a new ward
    """

    if request.method == "GET":
        wards = Ward.objects.all()
        serializer = WardSerializer(wards, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = WardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def ward_detail(request, pk):
    """
    Retrieve, update or delete a ward
    """
    try:
        ward = Ward.objects.get(pk=pk)
    except Ward.DoesNotExist:
        return Response(
            {"error": "Ward not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = WardSerializer(ward)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = WardSerializer(ward, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        ward.delete()
        return Response(
            {"message": "Ward deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


#Bed Views
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def bed_create(request):
    if request.method == "GET":
        beds = Bed.objects.select_related("ward")
        return Response(BedSerializer(beds, many=True).data)

    serializer = BedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)