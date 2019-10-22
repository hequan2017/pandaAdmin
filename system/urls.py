from django.urls import path
from system.views import  UserInfo, UserLogout, TestList,TestDetail

app_name = "system"

urlpatterns = [
    path('user_info', UserInfo.as_view()),
    path('logout', UserLogout.as_view()),
    path('test', TestList.as_view()),
    path('test/<int:pk>', TestDetail.as_view())
]
