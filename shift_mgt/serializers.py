from rest_framework import serializers
from .models import Shift
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


class ShiftSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Shift
        fields = [
            "id",
            "user",
            "role",
            "date",
            "start_time",
            "end_time",
            "shift_type",
            "assigned_by",
            "created_at",

            # extras
            "user_full_name",
            "user_email",
        ]
        read_only_fields = ["assigned_by", "created_at"]

    
    # for extracting users name
    def get_user_full_name(self, obj):
        user = obj.user
        if not user:
            return None

        # Handle users who don't have surname field
        first = getattr(user, "first_name", "")
        last = getattr(user, "last_name", "")
        surname = getattr(user, "surname", "")

        full_name = f"{first} {surname} {last}".strip()
        return full_name or user.username

    # Validate end_time > start_time
    def validate(self, attrs):
        start = attrs.get("start_time")
        end = attrs.get("end_time")

        if start and end and end <= start:
            raise serializers.ValidationError(
                "End time must be greater than start time."
            )

        return attrs

    # Validate shift overlapping
    def validate(self, attrs):
        attrs = super().validate(attrs)

        user = attrs.get("user")
        date = attrs.get("date")
        start = attrs.get("start_time")
        end = attrs.get("end_time")

        existing = Shift.objects.filter(user=user, date=date, start_time=start, end_time=end)
        
        #exclude current shift
        if self.instance:
            existing = existing.exclude(id=self.instance.id)

        if existing.filter(
            start_time__lt=end,
            end_time__gt=start
        ).exists():
            raise serializers.ValidationError(
                "This user already has an overlapping shift."
            )

        return attrs

    
    def create(self, validated_data):
        request = self.context.get("request")
        user = validated_data["user"]
        
        # Auto-assign admin/creator
        if request and request.user.is_authenticated:
            validated_data["assigned_by"] = request.user
        
        shift = super().create(validated_data)
        
        # Send shift email notification
        subject = "Shift Assigned"
        message = (
            f"Dear {user.first_name},\n\n"
            f"You have been assigned a shift:\n"
            f"Date: {shift.date}\n"
            f"Time: {shift.start_time} - {shift.end_time}\n"
            f"Role: {shift.role}\n\n"
            f"Assigned by: {shift.assigned_by.first_name}\n\n"
            "Please log in to your dashboard for details."
        )

        if user.email:
            send_mail(subject, message, "no-reply@hospital.com", [user.email])

        return shift



# from rest_framework import serializers
# from .models import Shift
# from django.contrib.auth import get_user_model
# from django.utils import timezone

# User = get_user_model()


# class ShiftSerializer(serializers.ModelSerializer):
#     # Build full name manually (read-only)
#     user_full_name = serializers.SerializerMethodField()
#     user_email = serializers.EmailField(source="user.email", read_only=True)

#     class Meta:
#         model = Shift
#         fields = [
#             "id",
#             "user",
#             "role",
#             "date",
#             "start_time",
#             "end_time",
#             "shift_type",
#             "assigned_by",
#             "created_at",

#             # extras (read-only display fields)
#             "user_full_name",
#             "user_email",
#         ]
#         read_only_fields = ["assigned_by", "created_at"]

#     # Validate that end_time is after start_time
#     def validate(self, attrs):
#         start = attrs.get("start_time")
#         end = attrs.get("end_time")

#         if start and end and end <= start:
#             raise serializers.ValidationError(
#                 "End time must be greater than start time."
#             )

#         return attrs

# Prevent overlapping shifts for the same user
#     def validate(self, attrs):
#         attrs = super().validate(attrs)

#         user = attrs.get("user")
#         date = attrs.get("date")
#         start = attrs.get("start_time")
#         end = attrs.get("end_time")

#         # This logic ignores the instance being updated
#         existing = Shift.objects.filter(user=user, date=date)
#         if self.instance:
#             existing = existing.exclude(id=self.instance.id)

#         if existing.filter(
#             start_time__lt=end,
#             end_time__gt=start
#         ).exists():
#             raise serializers.ValidationError(
#                 "This user already has a shift that overlaps with the given time range."
#             )

#         return attrs

#     # Auto-assign 'assigned_by' field from request user
#     def create(self, validated_data):
#         request = self.context.get("request")
#         if request and request.user.is_authenticated:
#             validated_data["assigned_by"] = request.user

#         return super().create(validated_data)
    
    

# Display user full name & email easily (read-only)
 # user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)
# user_email = serializers.EmailField(source="user.email", read_only=True)