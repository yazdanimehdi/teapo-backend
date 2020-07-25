from rest_framework import serializers
from institutions.models import Users
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = Users
        exclude = ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined']

    def get_token(self, model):
        return Token.objects.get(user=model).key

    def create(self, validated_data):

        if validated_data['role'] == 1:
            user = super(UserSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
            Token.objects.get_or_create(user=user)
            return user

        if validated_data['role'] == 2 or validated_data['role'] == 3:
            if self.context['request'].user.role == 4:
                user = super(UserSerializer, self).create(validated_data)
                user.set_password(validated_data['password'])
                user.save()
                Token.objects.get_or_create(user=user)
                return user

        if validated_data['role'] == 4:
            if self.context['request'].user.role == 5:
                user = super(UserSerializer, self).create(validated_data)
                user.set_password(validated_data['password'])
                user.save()
                Token.objects.get_or_create(user=user)
                return user
        else:
            self.error_messages['permission'] = 'You do not have permission to perform this action.'
            return super(UserSerializer, self).fail('permission')
