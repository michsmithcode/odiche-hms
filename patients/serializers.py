# serializers.py
from rest_framework import serializers
from .models import PatientProfile
from .utils import generate_reg_no, generate_file_folder_no, generate_card_number


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"
        read_only_fields = ["reg_no", "file_folder_no", "card_no", "user", "is_verified"]

    def create(self, validated_data):
        validated_data["reg_no"] = generate_reg_no()
        validated_data["file_folder_no"] = generate_file_folder_no()
        validated_data["card_no"] = generate_card_number()

        return super().create(validated_data)








# from rest_framework import serializers
# from .models import PatientProfile


# class PatientProfileSerializer(serializers.ModelSerializer):
#     full_name = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = PatientProfile
#         fields = [
#             "id",
#             "card_no",
#             "first_name",
#             "middle_name",
#             "last_name",
#             "full_name",
#             "state",
#             "date_of_birth",
#             "contact_number",
#             "emergency_contact_name",
#             "emergency_contact_number",
#             "gender",
#             "address",
#             "created_at",
#             "is_verified",
#         ]
#         read_only_fields = ["card_no", "created_at", "is_verified"]

#     def get_full_name(self, obj):
#         parts = [obj.first_name, obj.middle_name, obj.last_name]
#         return " ".join([x for x in parts if x])

