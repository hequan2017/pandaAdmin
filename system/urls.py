from django.urls import path
from system.views import logout_view, UserInfo, UserLogout,Menu

app_name = "system"

urlpatterns = [
    path('logout', logout_view, name="logout"),
    path('api/user_info', UserInfo.as_view()),
    path('api/logout', UserLogout.as_view()),
    path('menu',Menu.as_view())
]
