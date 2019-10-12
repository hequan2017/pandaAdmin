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
            'avatar': 'https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png'
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


class Menu(APIView):

    def post(self, request):
        result = [

            {
                "path": '/assets',
                "name": 'assets',
                "meta": {
                    "icon": 'md-menu',
                    "title": '资产管理'
                },
                "component": 'Main',
                "children": [
                    {
                        'path': 'ecs',
                        'name': 'ecs',
                        'meta': {
                            'access': ['assets.view_ecs'],
                            'icon': 'md-funnel',
                            'title': 'ecs'
                        },
                        'component': 'assets/ecs/ecs-list'
                    }
                ]
            },
            # {
            #     "path": '/multilevel',
            #     "name": 'multilevel',
            #     "meta": {
            #         "icon": 'md-menu',
            #         "title": '多级菜单'
            #     },
            #     "component": 'Main',
            #     "children": [
            #         {
            #             "path": '/level_2_1',
            #             "name": 'level_2_1',
            #             "meta": {
            #                 "icon": 'md-funnel',
            #                 "title": '二级-1'
            #             },
            #             "component": 'multilevel/level-2-1'
            #         },
            #
            #     ]
            # },
            {
                "path": '/k8s',
                "name": 'k8s',
                "meta": {
                    "icon": 'md-menu',
                    "title": '多级菜单'
                },
                "component": 'Main',
                "children": [
                    {
                        "path": '/pods',
                        "name": 'pods',
                        "meta": {
                            "icon": 'md-funnel',
                            "title": 'pods',
                        },
                        "component": 'k8s/k8s-pods'
                    },
                    {
                        "path": '/webssh/:name/:namespace',
                        "name": 'webssh',
                        "meta": {
                            "icon": 'md-funnel',
                            "title": 'webssh',
                            "hideInMenu": "true",
                        },
                        "component": 'k8s/k8s-webssh'
                    }

                ]
            }
        ]
        return HttpResponse(json.dumps(result))


def logout_view(request):
    """
    注销
    :param request:
    :return:
    """
    logout(request)
    return redirect('system:login')


class DisableCSRFCheck(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
