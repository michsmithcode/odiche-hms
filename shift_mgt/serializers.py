from rest_framework import serializers
from .models import Shift
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ShiftSerializer(serializers.ModelSerializer):
    # Build full name manually (read-only)
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

            # extras (read-only display fields)
            "user_full_name",
            "user_email",
        ]
        read_only_fields = ["assigned_by", "created_at"]

    # Validate that end_time is after start_time
    def validate(self, attrs):
        start = attrs.get("start_time")
        end = attrs.get("end_time")

        if start and end and end <= start:
            raise serializers.ValidationError(
                "End time must be greater than start time."
            )

        return attrs

    # Optional: Prevent overlapping shifts for the same user
    def validate(self, attrs):
        attrs = super().validate(attrs)

        user = attrs.get("user")
        date = attrs.get("date")
        start = attrs.get("start_time")
        end = attrs.get("end_time")

        # This logic ignores the instance being updated
        existing = Shift.objects.filter(user=user, date=date)
        if self.instance:
            existing = existing.exclude(id=self.instance.id)

        if existing.filter(
            start_time__lt=end,
            end_time__gt=start
        ).exists():
            raise serializers.ValidationError(
                "This user already has a shift that overlaps with the given time range."
            )

        return attrs

    # Auto-assign 'assigned_by' field from request user
    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["assigned_by"] = request.user

        return super().create(validated_data)

# Display user full name & email easily (read-only)
 # user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)
# user_email = serializers.EmailField(source="user.email", read_only=True)