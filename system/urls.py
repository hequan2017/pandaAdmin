from django.urls import path
from system.views import logout_view, UserInfo, UserLogout,Menu, TestList,TestDetail

app_name = "system"

urlpatterns = [
    path('logout', logout_view, name="logout"),
    path('api/user_info', UserInfo.as_view()),
    path('api/logout', UserLogout.as_view()),
    path('menu',Menu.as_view()),

    path('test', TestList.as_view()),
    path('test/<int:pk>', TestDetail.as_view()),
]
