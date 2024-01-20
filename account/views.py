from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, get_object_or_404, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from account.models import Application, ProgramingLanguage, SendRequestToEmail
from account.serializers import (ApplicationSerializer, RegisterApplicationSerializer, ConfirmRequestSerializer,
                                 ProgramingLanguageSerializer)

from account.services import SendRequestToEmailManager


class ProgramingLanguageViewSet(ModelViewSet):
    queryset = ProgramingLanguage.objects.all()
    serializer_class = ProgramingLanguageSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    permission_classes = (AllowAny, )


class RegisterGenericAPIView(GenericAPIView):
    serializer_class = RegisterApplicationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        manager = SendRequestToEmailManager(application)
        manager.send_key()
        application_serializer = ApplicationSerializer(instance=application, context={'request': request})
        return Response({
            **application_serializer.data,
        })


class ConfirmEmailApiView(GenericAPIView):
    serializer_class = ConfirmRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data.get('key', None)
        confirm = serializer.validated_data.get('confirm', None)
        application = get_object_or_404(SendRequestToEmail, key=key).application
        manager = SendRequestToEmailManager(application)
        is_confirmed = manager.confirm(key, confirm)
        if is_confirmed:
            application.is_confirmed = True
        return Response(
            {'is_confirmed': is_confirmed},
            status=status.HTTP_202_ACCEPTED if is_confirmed or not is_confirmed else status.HTTP_400_BAD_REQUEST
        )
