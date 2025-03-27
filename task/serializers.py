from rest_framework import serializers

from account.models import User
from account.serializers import UserSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False)

    def validate(self, attrs):
        if attrs.get('assigned_to_id') and not User.objects.filter(id=attrs.get('assigned_to_id')).exists():
            raise serializers.ValidationError({'assigned_to_id': ['This user does not exist']})
        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Task
        fields = '__all__'
