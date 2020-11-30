from django.urls import path, re_path, include

from uauth.views import home, register, user_login

app_name = 'uauth'

urlpatterns = [
    re_path (r"^home/", home, name="home"),
	re_path (r"^accounts/", include("django.contrib.auth.urls")),
	re_path (r'^register/$',  register,  name='register'),
 	re_path (r'^user_login/$',user_login,name='user_login'),
]
