from pandas import pandas as pd
import numpy as np
import datetime as dt
import pytz

from django.utils import timezone
from django.utils.timezone import make_aware

from todo.models import Todo, Resource#, Context, TodoStatus, ResourceGroup
from django.db.models import F, Q
from django.db.models.functions import TruncDate, Coalesce

WEEKENDS  = [4,5]
HOLIDAYS  = ['2020-12-02','2020-12-03']
date_format = '%d-%b-%Y %H:%M:%S'
def get_heatmap(startDate, offset):
	try:
		dt_start = dt.datetime.strptime(startDate + " 00:00:00", date_format) + dt.timedelta(days=int(offset))
	except Exception as e:
#		print ("Error", e)
		dt_start = dt.datetime.strptime(dt.date.today().strftime('%d-%b-%Y') + " 00:00:00", date_format)

	dt_end   = dt.datetime.strptime ((dt_start + dt.timedelta(days=30)).strftime ('%d-%b-%Y 23:59:59'), date_format)

	dt_start = pytz.utc.localize(dt_start)
	dt_end   = pytz.utc.localize(dt_end)

	print ("Start>>", dt_start,	"End>>", dt_end)

	df = pd.DataFrame ({'AllDate': pd.date_range(start = dt_start, periods = 30)})
	df ['AllDate'] = df['AllDate'].dt.normalize()
	df ['heatmap'] = [
    	0 if x.weekday() not in WEEKENDS else -1 for x in df['AllDate']
	]
	df ['dispday'] = df.apply (lambda x: int(x.AllDate.strftime('%Y%m%d')),axis=1)
	df.heatmap = df.apply (lambda x: -3 if x.AllDate.strftime('%Y-%m-%d') in HOLIDAYS else x.heatmap,axis=1)

	qs_res = Resource.objects.annotate (
		login_id = F('user__username')
		).values ('login_id'
#		).filter (user__username__in = {'gkumar'}
		).order_by('user')

	df_res = pd.DataFrame()
	for x in list(qs_res):
		df_tmp = df.copy()
		df_tmp ['login_id'] = x ['login_id']
		df_res = df_res.append (df_tmp, ignore_index = True)

	filters = Q()
#	filters = Q(assigned_to__user__username__in = {'gkumar', 'jmittameda'})
	filters.add (Q(Q (start_date__range = [dt_start, dt_end]) |
			Q(end_date__range = [dt_start, dt_end])), Q.AND)
#	print ("Filtersss>>>>", filters)
	qs_todo = Todo.objects.annotate (
		login_id = F('assigned_to__user__username')
		).annotate(s_date=TruncDate('start_date'), e_date=TruncDate('end_date')
		).values ('login_id', 's_date', 'e_date', 'short_desc'
		).filter (
			filters
		).order_by ('assigned_to', 'start_date','end_date')

	ll = list(qs_todo)
#	print (ll, type (ll))
	for x in ll:
#		print (x ['s_date'],"-",x ['e_date'].strftime('%Y%m%d'), type (x ['e_date']), type (x))
		x ['ne_date'] = None if x ['e_date'] is None else int(x ['e_date'].strftime('%Y%m%d'))
		x ['ns_date'] = None if x ['s_date'] is None else int(x ['s_date'].strftime('%Y%m%d'))
#		print (x ['login_id'], x ['ns_date'], x ['ne_date'])
		df_res.heatmap = df_res.apply (lambda p: 
			-2 if p.heatmap == 0 and
				 p.login_id == x ['login_id'] and
				 'Leave' == x ['short_desc'] and
				(
				  ((x ['ns_date'] is not None and p.dispday >= x ['ns_date']) and (x ['ne_date'] is not None and p.dispday <= x ['ne_date'])) or
				  (x ['ns_date'] is not None and x ['ne_date'] is None and p.dispday == x ['ns_date']) or
				  (x ['ne_date'] is not None and x ['ns_date'] is None and p.dispday == x ['ne_date'])
				)
			else p.heatmap,axis=1)

		df_res.heatmap = df_res.apply (lambda p: 
			p.heatmap+1 if p.heatmap >= 0 and
				 p.login_id == x ['login_id'] and
				(
				  ((x ['ns_date'] is not None and p.dispday >= x ['ns_date']) and (x ['ne_date'] is not None and p.dispday <= x ['ne_date'])) or
				  (x ['ns_date'] is not None and x ['ne_date'] is None and p.dispday == x ['ns_date']) or
				  (x ['ne_date'] is not None and x ['ns_date'] is None and p.dispday == x ['ne_date'])
				)
			else p.heatmap,axis=1)

#	print(df_res.ffill())		

	df ['dispday'] = df ['dispday'].astype(str)
	df_res_T = pd.crosstab(index=df_res['login_id'], columns=df_res['dispday'], values=df_res['heatmap'], aggfunc='sum')
	df_res_T.reset_index(inplace=True)

	return [df_res_T.columns, df_res_T.values, dt_start.strftime('%d-%b-%Y')] #df_res_T.values
