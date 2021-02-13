from rest_framework import serializers

from user_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        new_profile = self.Meta.model(**validated_data)

        if password:
            new_profile.set_password(password)
            new_profile.save()
        else:
            raise ValueError('При создании пользователя не был указан пароль')

        return new_profile

    def update(self, instance: Profile, validated_data):
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)
        instance.save()

        return instance
