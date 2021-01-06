from django.http import HttpResponse, Http404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from dal import autocomplete
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from .forms import TodoForm
from .models import Todo, Resource, Context, TodoStatus, ResourceGroup
import util.uctutil as uu

#home view for posts. Posts are displayed in a list
class TodoIndexView(ListView):
  model = Todo
  template_name='todo/todo_index.html'
  context_object_name = 'todo_list'
  paginate_by = 15


  def get_queryset(self):
    # param_page = self.request.GET.get ('page')
    # if (param_page):
    #   print ("1---------->Page Param found in request")
      # qs = super().get_queryset()
      # print ("2---------->QS Count at Pagination", len(qs))
      # return qs;
    filters = Q()
    grp = ResourceGroup.objects.values ('group').filter (
          user__username =self.request.user, can_see_group_list=True)

    filter_param = self.request.GET.get ('filter', self.request.session.get ('filter_val', 'mylist'))
    if filter_param == 'mylist' or filter_param == self.request.user.username:
      filter_param = 'mylist'
    elif grp.count() == 0 and (filter_param == 'grplist' or filter_param != self.request.user.username):
      if self.request.session['filter_val']:
        self.request.session['filter_val'] = 'mylist'
      raise Http404 ("Not found")

    self.request.session['filter_val'] = filter_param
    if (filter_param=='mylist'):
      filters = Q(assigned_to__user=self.request.user)
      filters.add (Q(Q (added_user__user=self.request.user) & Q(assigned_to__user__isnull=True)), Q.OR)
    elif (filter_param=='grplist'):
      filters = Q(group__id__in=grp)
    else: # Assume parameter is for Assign To
      filters = Q(group__id__in=grp)
      filters.add (Q(assigned_to__user__username=filter_param), Q.AND)

    ## Append base status filter for Status [All/Completed/Non-Completed]
    status_param = self.request.GET.get ('status', self.request.session.get ('status_val', 'open'))
    if status_param == 'all':
      # No filter based on status
      self.request.session['status_val'] = status_param
    elif status_param == 'completed':
      self.request.session['status_val'] = status_param
      filters.add (Q(status_id__code='COM'), Q.AND)
    else:
      self.request.session['status_val'] = status_param
      filters.add (~Q(status_id__code='COM'), Q.AND)

    print ('10---------->Filters', filters)
    
    ob = ['-added_date', 'context_id']
    qs = Todo.objects.filter (filters).order_by(*ob)
    return qs

  def get_context_data(self, **kwargs):
    context = super(TodoIndexView, self).get_context_data(**kwargs)
    context['filter'] = self.request.GET.get('filter', 'mylist')
    users = Resource.objects.filter(
      user__in = ResourceGroup.objects.values ('user').filter(
        group__in=ResourceGroup.objects.values ('group').filter (
          user__username =self.request.user, can_see_group_list=True))).order_by ("res_name")
    context['res'] = users
    return context    

class ContextAutocomplete(autocomplete.Select2QuerySetView):
  def get_queryset(self):
  # Don't forget to filter out results depending on the visitor !
  #if not self.request.user.is_authenticated:
  #  return Resource.objects.none()

    qs = Context.objects.all().order_by('-context_id')
    if self.q:
      qs = qs.filter(Q(context_id__icontains=self.q) | Q(context_name__icontains=self.q)).order_by('-context_id')

    return qs

#Detail view (view post detail)
class TodoDetailView(DetailView):
  model=Todo
  template_name = 'todo/todo_detail.html'

@login_required
def todo_create(request):
  form = TodoForm(request.user, 'create', request.POST or None)
  if request.method == 'POST':
    form = TodoForm(request.user, 'create', request.POST)
    if form.is_valid():
      instance = form.save (commit=False)
      print ('Adding record--------------->', request.user)
      instance.added_user = Resource.objects.filter(user=request.user).first()
      instance.save()
      return redirect('todo_index')

  return render(request,'todo/todo_create.html',{'form': form})

@login_required (redirect_field_name='next')
def todo_close(request, pk, template_name='todo/todo_close.html'):
    todo = get_validated_todo (pk, request.user)    
    form = TodoForm(request.user, 'close', request.POST or None, instance=todo)
    form.fields['created_by'].initial = todo.added_user
    if form.is_valid():
        instance = form.save (commit=False)
        instance.status = TodoStatus.objects.filter (code='COM').first()
        instance.save()
        next = request.GET.get("next", None)
        if next is None:
          print ('Next is none.............')
          return redirect('todo_index')
        else:
          print ('Next is Not none.............', next)
          return redirect (next)

    return render(request, template_name, {'form':form})

@login_required (redirect_field_name='next')
def todo_edit(request, pk, template_name='todo/todo_edit.html'):
    todo = get_validated_todo (pk, request.user)
#    todo= get_object_or_404(Todo, pk=pk)
    form = TodoForm(request.user, 'edit', request.POST or None, instance=todo)
    form.fields['created_by'].initial = todo.added_user
    if form.is_valid():
        form.save()
        next = request.GET.get("next", None)
        if next is None:
          print ('Next is none.............')
          return redirect('todo_index')
        else:
          print ('Next is Not none.............', next)
          return redirect (next)

    return render(request, template_name, {'form':form})

@login_required (redirect_field_name='next')
def todo_copyas(request, pk, template_name='todo/todo_copyas.html'):
    todo = get_validated_todo (pk, request.user)
    todo.pk = None
    form = TodoForm(request.user, 'copyas', request.POST or None, instance=todo)
    form.fields['created_by'].initial = todo.added_user
    if form.is_valid():
        instance = form.save (commit=False)
        instance.added_user = Resource.objects.filter(user=request.user).first()
        instance.added_date = None
        instance.save()
        next = request.GET.get("next", None)
        if next is None:
          print ('Next is none.............')
          return redirect('todo_index')
        else:
          print ('Next is Not none.............', next)
          return redirect (next)
    return render(request, template_name, {'form':form})

@login_required
def todo_delete(request, pk, template_name='todo/todo_delete.html'):
    todo = get_validated_todo (pk, request.user)
    form = TodoForm(request.user, 'delete', request.POST or None, instance=todo)    
    form.fields['created_by'].initial = todo.added_user
    if form.is_valid():
        todo.delete()
        next = request.GET.get("next", None)
        if next is None:
          print ('Next is none.............')
          return redirect('todo_index')
        else:
          print ('Next is Not none.............', next)
          return redirect (next)
    return render(request, template_name, {'form':form})

@login_required
def todo_heatmap(request, template_name='todo/todo_heatmap.html'):
    start_param = request.GET.get ('start_date', None)
    offset      = request.GET.get ('offset', None)
    hm_list = uu.get_heatmap (start_param, offset)
#    print (hm_list)
#    return render(request, template_name, {'hm_list':hm_list.items()})
    return render(request, template_name, {'hm_list':hm_list})

def get_validated_todo (pk, user):
    filters = Q()
    grp = ResourceGroup.objects.values ('group').filter (
          user__username =user, can_edit_group_list=True)

    filters = Q(Q(pk=pk) & 
                Q(Q(assigned_to__user=user) | 
                  Q(Q(added_user__user=user) & Q(assigned_to__user__isnull=True)) |
                  Q(group__id__in=grp)))
    print (filters)
    return get_object_or_404(Todo, filters)
#    return Todo.objects.get(filters)
