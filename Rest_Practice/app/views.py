import uuid

from django.core.cache import cache
from rest_framework import exceptions, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Rest_Partice.settings import HTTP_ACTION_REGISTER, HTTP_ACTION_LOGIN
from app.auth import LoginAuthentication
from app.models import User, Address
from app.permissions import RequireLoginPermission
from app.serializers import UserSerializer, AddressSerializer
from app.throttles import Throttle


class UsersAPIView(CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")
        if action == HTTP_ACTION_REGISTER:
            return self.create(request, *args, **kwargs)

        if action == HTTP_ACTION_LOGIN:
            name = request.data.get('u_name')
            password = request.data.get('u_password')
            try:
                user = User.objects.get(u_name=name)
            except User.DoesNotExist:
                raise exceptions.NotFound
            if user.u_password == password:
                token = uuid.uuid4().hex
                cache.set(token, user.id)
                data = {
                    'msg': 'login success',
                    'status': 200,
                    'name': name,
                    'token': token
                        }
                return Response(data)
            else:
                raise exceptions.AuthenticationFailed

        else:
            raise exceptions.ParseError


class UserAPIView(RetrieveAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (LoginAuthentication,)
    permission_classes = (RequireLoginPermission, )
    throttle_classes = (Throttle,)
    throttle_rates = {
        'user': '5/m',
    }

    def retrieve(self, request, *args, **kwargs):

        if request.user.id != int(kwargs.get('pk')):
            raise exceptions.PermissionDenied
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AddressesViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    authentication_classes = (LoginAuthentication,)
    permission_classes = (RequireLoginPermission, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        a_id = serializer.data.get('id')
        address = Address.objects.get(pk=a_id)
        user = request.user
        address.a_user = user

        address.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset.filter(a_user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.a_user != request.user:
            raise exceptions.PermissionDenied
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
