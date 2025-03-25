from rest_framework import serializers

from account.models import User, Permission, Role


class UserSerializer(serializers.ModelSerializer):
    role_title = serializers.SerializerMethodField(read_only=True)

    def get_role_title(self, obj):
        if obj.role:
            return obj.role.title
        return None

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
        fields = ('id', 'name', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    permissions_list = PermissionSerializer(
        source='permissions',
        many=True,
        read_only=True
    )

    class Meta:
        model = Role
        fields = '__all__'


class AuthUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}
