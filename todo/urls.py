from django.views.static import serve
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('todo/',                 login_required(views.TodoIndexView.as_view()),  name='todo_index'),
	path('todo_detail/<int:pk>/', login_required(views.TodoDetailView.as_view()), name='todo_detail'),
	path('todo_create/',          views.todo_create,              name='todo_create'),	
	path('todo_edit/<int:pk>/',   views.todo_edit,                name='todo_edit'),
	path('todo_copyas/<int:pk>/', views.todo_copyas,              name='todo_copyas'),	
	path('todo_delete/<int:pk>/', views.todo_delete,              name='todo_delete'),
	path('todo_close/<int:pk>/',  views.todo_close,               name='todo_close'),

	re_path (r'^todo_heatmap/$',                      views.todo_heatmap,  name='todo_heatmap'),
	re_path (r'^todo_heatmap/(?P<start_date>\w+)/$',  views.todo_heatmap,  name='todo_heatmap'),

	re_path(
		r'^static/(?P<path>.*)$',
		serve,
		{'document_root': settings.STATIC_ROOT}), 
	re_path(
		r'^context-autocomplete/$',
		views.ContextAutocomplete.as_view (),
		name='context-autocomplete',
	),
]
