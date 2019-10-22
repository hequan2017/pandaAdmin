import logging
import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from system.models import Users
from django.urls import reverse_lazy
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from system.models import Test
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from system.serializers import TestSerializer
logger = logging.getLogger('system')


#         drf 中文文档   http://drf.jiuyou.info/#/drf/requests
class TestList(generics.ListCreateAPIView):
    queryset = Test.objects.get_queryset().order_by('id')
    serializer_class = TestSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('id', 'date','name')
    search_fields = ('id', 'name',)
    permission_classes = (permissions.DjangoModelPermissions,)  # 继承 django的权限


class TestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.get_queryset().order_by('id')
    serializer_class = TestSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class UserInfo(APIView):
    """
    获取用户信息
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = (json.loads(request.body))['token']
        obj = Token.objects.get(key=token).user
        result = {
            'name': obj.username,
            'user_id': obj.id,
            'access': list(obj.get_all_permissions()) + ['admin'] if obj.is_superuser else list(
                obj.get_all_permissions()),
            'token': token,
            'avatar': ''
        }
        return HttpResponse(json.dumps(result))


class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = (json.loads(request.body))['token']
        obj = Token.objects.get(key=token)
        obj.delete()
        result = {
            "status": True
        }
        return HttpResponse(json.dumps(result))


class DisableCSRFCheck(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
