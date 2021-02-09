from django.urls import path, re_path, include
from uauth.views import home, uregister, ulogin, upassword, ulogout

app_name = 'uauth'

urlpatterns = [
	re_path (r"^accounts/" , include("django.contrib.auth.urls")),

	re_path (r'^$',     home, name="home_index"),    
    re_path (r"^home/", home, name="home"),

    re_path (r'^logout/$'  , ulogout,   name='logout'),
	re_path (r'^register/$', uregister, name='register'),
 	re_path (r'^login/$'   , ulogin,    name='login'),
    re_path (r'^password/$', upassword, name='password'),

]
