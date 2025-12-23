from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PharmacistProfile
from .serializers import PharmacistProfileSerializer




#=========permission access control for pharmacists
from permissions.decorators import permission_required

#Pharmacist permission
@permission_required("can_dispense_drugs")
def dispense_drug(request):
    return Response({"message": "Pharmacist dispensed medication"})


@permission_required("can_manage_stock")
def update_stock(request):
    return Response({"message": "Stock updated"})



# Pharmacists self-profile operations
@api_view(["GET", "PATCH", "PUT"])
@permission_classes([IsAuthenticated])
def pharmacist_profile(request):
    try:
        profile = PharmacistProfile.objects.get(user=request.user)
    except PharmacistProfile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PharmacistProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method in ["PATCH", "PUT"]:
        serializer = PharmacistProfileSerializer(profile, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# pharmacist CRUD by admin only permission 

@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def admin_list_pharmacists(request):
    pharmacists = PharmacistProfile.objects.all()
    serializer = PharmacistProfileSerializer(pharmacists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def admin_get_pharmacist(request, pk):
    pharmacist = get_object_or_404(PharmacistProfile, pk=pk)
    serializer = PharmacistProfileSerializer(pharmacist)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
def admin_create_pharmacist(request):
    serializer = PharmacistProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["PUT", "PATCH"])
@permission_classes([permissions.IsAdminUser])
def admin_update_pharmacist(request, pk):
    pharmacist = get_object_or_404(PharmacistProfile, pk=pk)
    serializer = PharmacistProfileSerializer(pharmacist, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
@permission_classes([permissions.IsAdminUser])
def admin_delete_pharmacist(request, pk):
    pharmacist = get_object_or_404(PharmacistProfile, pk=pk)
    pharmacist.delete()
    return Response({"message": "Pharmacist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



