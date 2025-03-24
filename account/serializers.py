from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
