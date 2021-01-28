from django.db import models
from django.contrib.auth.models import Group, User

class ResourceGroup (models.Model):
	user           = models.ForeignKey(User,on_delete=models.CASCADE)
	group          = models.ForeignKey(Group,on_delete=models.CASCADE)
	can_see_group_list   = models.BooleanField (default=False)
	can_edit_group_list  = models.BooleanField (default=False)

	class Meta:
		unique_together = ('user', 'group',)

	def __str__(self):
		return "User: "                 + self.user.username            + "\n" + \
		       "Group: "                + self.group.name               + "\n" + \
		       "can_edit_master_data: " + str(self.can_edit_master_data)  + "\n" + \
			   "can_see_group_list: "   + str(self.can_see_group_list)  + "\n" + \
			   "can_edit_group_list: "  + str(self.can_edit_group_list) + "\n"

class Resource (models.Model):
	user           = models.OneToOneField(User,on_delete=models.CASCADE)
	res_name       = models.CharField (max_length=120,null=True, blank=False)
	added_date     = models.DateTimeField (auto_now_add=True)
	portfolio_site = models.URLField(blank=True)
	profile_pic    = models.ImageField(upload_to='profile_pics',blank=True)
	can_edit_master_data = models.BooleanField (default=False)
	
	def __str__(self):
		return self.res_name + ' (' + self.user.username + ')'

class TodoStatus (models.Model):
	code   = models.CharField (max_length=60, blank=False, primary_key=True)
	name = models.CharField (max_length=120,null=True, blank=False)

	added_user   = models.ForeignKey ('Resource', on_delete=models.DO_NOTHING)
	added_date   = models.DateTimeField (auto_now_add=True)

	def __str__(self):
		return self.name

class TodoType (models.Model):
	code   = models.CharField (max_length=60, blank=False, primary_key=True)
	name = models.CharField (max_length=120,null=True, blank=False)

	added_user   = models.ForeignKey ('Resource', on_delete=models.DO_NOTHING)
	added_date   = models.DateTimeField (auto_now_add=True)

	def __str__(self):
		return self.name

class Context (models.Model):
	context_id   = models.CharField (max_length=60, blank=False, primary_key=True)
	context_name = models.CharField (max_length=120,null=True, blank=False)
	added_date   = models.DateTimeField (auto_now_add=True)

	def __str__(self):
		return self.context_id + ' (' + self.context_name + ')'

# Create your models here.
class Todo (models.Model):
	EFFORT_TYPES = (
		('H', 'Hour(s)'),
		('D', 'Day(s)'),
		('M', 'Month(s)'),
	)

	assigned_to  = models.ForeignKey ('Resource', on_delete=models.DO_NOTHING,  null=True, blank=True, related_name='assigned_to')
	context_id   = models.ForeignKey ('Context',  on_delete=models.DO_NOTHING,  null=True, blank=True)
	todo_type    = models.ForeignKey ('TodoType',  on_delete=models.DO_NOTHING, null=True, blank=True)
	short_desc   = models.CharField (max_length=200, help_text='Short description of the todo item ...', blank=True)
	effort_type  = models.CharField (max_length=1, choices=EFFORT_TYPES, null=True, blank=True)
	effort       = models.DecimalField (max_digits=5, decimal_places=0, null=True, blank=True)
	start_date   = models.DateTimeField (null=True, blank=True)
	end_date     = models.DateTimeField (null=True, blank=True)	
	status       = models.ForeignKey ('TodoStatus',  on_delete=models.DO_NOTHING, related_name='status', null=True, blank=True)
	group        = models.ForeignKey (Group,on_delete=models.DO_NOTHING, null=True, blank=True)

	added_user   = models.ForeignKey ('Resource', on_delete=models.DO_NOTHING, related_name='added_user', null=True, blank=True)
	added_date   = models.DateTimeField (auto_now_add=True)

	def __str__(self):
		return self.short_desc
