from django.urls import path
from .views import UserAPIView,SignupView,UserinfoView,ForgetIDView,ForgetPasswordView
from .views import checkDuplicatedID,checkDuplicatedNickname,token_refresh
from .views import getNickname,changePassword,myPosts,myComments,myLikes

app_name = "users"

urlpatterns = [
    path('refresh/',token_refresh,name='refresh'),

    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',UserAPIView.as_view(), name='login'),
    path('logout/',UserAPIView.as_view(), name='login'),
    path('api/check/id/',checkDuplicatedID,name='check_id'),
    path('api/check/nickname/',checkDuplicatedNickname,name='check_Name'),
    path('api/get/nickname/',getNickname,name='get_nickname'),

    path('userinfo/',UserinfoView.as_view(),name='get_userinfo'),
    path('userinfo/changepassword/',changePassword,name='change_password'),
    path('userinfo/myposts/',myPosts,name='myposts'),
    path('userinfo/mycomments/',myComments,name='mycomments'),
    path('userinfo/mylikes/',myLikes,name='mylikes'),

    path('forget_id/',ForgetIDView.as_view(),name='forget_id'),
    path('forget_password/',ForgetPasswordView.as_view(),name='forget_password'),

]