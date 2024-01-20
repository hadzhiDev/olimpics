from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError

from account.models import Application, ProgramingLanguage


class ProgramingLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramingLanguage
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = '__all__'


class RegisterApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {
            'full_name': {'required': True},
            'phone': {'required': True},
        }

    def validate(self, attrs):
        for item in attrs.items():
            if not item[1]:
                raise ValidationError({
                    item[0]: [
                        f'{item[0]} не может быть пустым'
                    ]
                })
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class ConfirmRequestSerializer(serializers.Serializer):

    key = serializers.UUIDField()

    confirm = serializers.BooleanField()


# class SendRequestSerializer(serializers.Serializer):
#
#     email = serializers.EmailField()