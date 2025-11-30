from django.shortcuts import render
from permissions.decorators import permission_required
# Create your views here.


#
#Patient
@permission_required("can_view_patient")
def patient_self_profile(request):
    return Response({"message": "Patient viewing own profile"})

