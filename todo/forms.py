from dal import autocomplete
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.models import Group, User
from datetime import date

from .models import Todo, TodoType, Resource, Context, TodoStatus, ResourceGroup, TodoNotes

STATES = (
	('', 'Choose...'),
	('MG', 'Minas Gerais'),
	('SP', 'Sao Paulo'),
	('RJ', 'Rio de Janeiro')
)

class ResourceForm (forms.ModelForm):
	class Meta():
		model = Resource
		fields = ('res_name', 'portfolio_site','profile_pic')

class TodoForm (forms.ModelForm):
	short_desc    = forms.CharField (widget = forms.TextInput (attrs={'autocomplete': 'off'}))
	group         = forms.ModelChoiceField(queryset=Group.objects.none(), required=False)
	assigned_to   = forms.ModelChoiceField(queryset=Resource.objects.none(), required=False)
	created_by    = forms.CharField (disabled=True, required=False)
	context_id    = forms.ModelChoiceField(queryset=Context.objects.all(), to_field_name='context_id',
					required=False, widget=autocomplete.ModelSelect2(url='context-autocomplete'))
	todo_type     = forms.ModelChoiceField(queryset=TodoType.objects.all().order_by('name'), to_field_name='code', required=False)
	status        = forms.ModelChoiceField(queryset=TodoStatus.objects.all().order_by('name'), to_field_name='code', required=False)
	start_date    = forms.DateField (input_formats=['%d-%b-%Y'],
                           label='Start Date',
                           required=False,
                           widget=forms.DateInput(
                                   format='%d-%b-%Y',
                                   attrs={'autocomplete': 'off', 'placeholder': 'Select a date', 'class': 'datepicker'})
                           )
	end_date   = forms.DateField (input_formats=['%d-%b-%Y'],
                           label='End Date',
                           required=False,
                           widget=forms.DateInput(
                                   format='%d-%b-%Y',
                                   attrs={'autocomplete': 'off', 'placeholder': 'Select a date', 'class': 'datepicker'})
                           )

	class Meta:
		model = Todo
		fields = [
			'assigned_to', 'group', 'context_id', 'todo_type','short_desc',
			'status','effort_type','effort','start_date', 'end_date',
		]

	def clean(self):
#		print ("Calling Clean Start date --> (1)")
		start_date = self.cleaned_data['start_date']
		end_date = self.cleaned_data['end_date']
		if start_date and end_date and end_date < start_date:
			raise forms.ValidationError('End Date cannot be before Start Date.')
#		print ("Calling Clean Start date --> (2)",start_date)
		super(TodoForm, self).clean()

	def __init__(self, user, mode, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.fields['group'].queryset = Group.objects.filter(user=user).all().order_by ("name")
		self.fields['assigned_to'].queryset = Resource.objects.filter(
			user__in = User.objects.filter(groups__in=Group.objects.filter(user=user))).order_by ("res_name")
		formAction = None
		if (mode=='delete'):
			formAction = Submit( 'save', 'Delete', css_class = 'btn btn-danger')
		elif (mode=='close'):
			formAction = Submit( 'save', 'Complete', css_class = 'btn btn-success')
		elif (mode=='copyas'):
			formAction = Submit( 'save', 'Copy', css_class = 'btn btn-info')			
		else:
			formAction = Submit( 'save', 'Save', css_class = 'btn btn-primary')

		self.helper.layout = Layout(
			Row(
				Column('short_desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('context_id', css_class='form-group col-md-12 mb-0'),				
				css_class='form-row'
			),			
			Row(
				Column('group', css_class='form-group col-md-4 mb-0'),
				Column('assigned_to', css_class='form-group col-md-5 mb-0'),
				Column('status',      css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),

			Row(
				Column('todo_type',   css_class='form-group col-md-4 mb-0'),
				Column('effort_type', css_class='form-group col-md-4 mb-0'),
				Column('effort',      css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),

			Row(
				Column('start_date', css_class='form-group col-md-4 mb-0'),
				Column('end_date',   css_class='form-group col-md-4 mb-0'),	
				Column('created_by', css_class='form-group col-md-4 mb-0'),			
				css_class='form-row'
			),
			Row(
        		Column (
        			FormActions(
        				formAction,
						HTML('<a class="btn btn-warning" href={% url "todo_index" %}>Cancel</a>'),
#            			Button( 'cancel', 'Cancel', css_class="btn btn-md btn-default",data_dismiss="modal")

            	),css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			)
		)

class TodoNotesForm (forms.ModelForm):
	class Meta():
		model = TodoNotes
		fields = ('todo', 'added_user', 'notes')
		widgets = {
			'todo': forms.HiddenInput(),
			'added_user': forms.HiddenInput(),
		}

#	def clean(self):
#		print ("Calling Clean Start date --> (1)")
#		self.cleaned_data['id_todo'] = 95
#		return super(TodoNotesForm, self).clean()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.layout = Layout (
			Row(
				Column(HTML('<textarea class="form-control" placeholder="Add a note here..." name="notes" id="notes" maxlength="300"></textarea>'),
					css_class='form-group col-md-11 mb-0'),
				Column(
				FormActions(
        			Submit( 'post', 'Post', css_class = 'btn btn-success')),
					css_class='form-group col-md-1 mb-0'),
				css_class='form-row'
			),
			Row (
				Column('todo'),
				Column('added_user'),
			)
		)

#######################################################
class TodoNForm (forms.ModelForm):
	class Meta:
		model = Todo
		fields = [
			'short_desc',		
			'assigned_to',
			'context_id',
			'status',
			'effort_type',
			'effort',
			'start_date',

		]
#		fields = "__all__"

	def clean(self):
		cleaned_data = super().clean()
		short_desc  = cleaned_data.get("short_desc")
		assigned_to = cleaned_data.get("assigned_to")
		if not (short_desc):
			self.add_error('short_desc', "Short Description is empty")
		if not (assigned_to):
			self.add_error('assigned_to', "Assigned To is empty")

		return cleaned_data