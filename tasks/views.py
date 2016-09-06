from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .models import Article
import json
from django.core import serializers

def index(request):
	items = Task.objects.all()
	return render_to_response('tasks/tasks_grid.html',{'items':items, 'username': 'username'})

@csrf_exempt
def get_articles(request):
	if request.method == 'POST':
		id_task = request.POST['id_task']
		queryset = Article.objects.filter(task_id=id_task)
		list = []
		for row in queryset:
		    list.append({'name':row.name, 'competitor': row.competitor.name, 'price': row.price, 'group': row.group.name})
		arts_list_json = json.dumps(list)
		return HttpResponse(arts_list_json, 'application/javascript')
	else:
		return json.dumps('{"error": "Wrong request"}')


@csrf_exempt
def get_tasks_mobile(request):
	if request.method == 'POST':
		uuid = request.POST['uuid']
		querysetTasks = Task.objects.all()
		t_ids = []
		for t in querysetTasks:
			if t.mobileDevice.uuid == uuid:
				t_ids.append(t.id)

		querysetArts = Article.objects.filter(task_id__in=t_ids)
		list = []
		for article in querysetArts:
			art = {
	            'task_name': article.task.name,
	            'id_task': article.task.id_task,
	            'enddate': article.task.end_date,
	            'begindate': article.task.begin_date,
	            'change_passwd': article.task.mobileDevice.change_password,
	            "compname": article.competitor.name,
	            "address": article.competitor.address,
	            "id_gr20": article.group.id,
	            "gr20": article.group.name,
	            'id_taskart': article.id,
	            'artname': article.name,
	            'pricefrom': article.pricefrom,
	            'priceto': article.priceto,
	            'id_unit': article.unit,
	            'quant': article.quant,
	            'takephoto': article.takephoto,
	        }
			list.append(art)
		arts_list_json = json.dumps(list)
		return HttpResponse(arts_list_json, 'application/javascript')
	else:
		return json.dumps('{"error": "Wrong request"}')

@csrf_exempt
def login_mobile(request):
	if request.method == 'POST':
		uuid = request.POST['uuid']
		pw = request.POST['pw'] # todo hash
		queryset = mobileDevice.objects.filter(uuid=uuid).filter(password=pw)
		if len(queryset)>0:
			return HttpResponse('1', 'application/javascript')
		else:
			return HttpResponse('0', 'application/javascript')
	else:
		return json.dumps('{"error": "Wrong request"}')

@csrf_exempt
def set_tasks_mobile(request):
	pass


# def getAddParams(imei):
#     con = model.db.connect()
#     cur = con.cursor()

#     def add_to_result(result):
#         result.append({'id_taskart': res[i]['id_taskart'],'add_params': [{'name_add': res[i]['name_add'],\
#         'adddatatype': res[i]['adddatatype'],'vvalue': [res[i]['vvalue']],'required': res[i]['required']},]})

#     selectAddParamsSql = """
#         select id_taskart, name_add, adddatatype, vvalue, required
#         from table(cpms.producer_addition_fnc(:imei))
#         order by id_taskart, name_add
#     """

#     result = []
#     values_for_this_id_a_param = []
#     additional_param_for_this_id_taskart = []
#     res = cur.execute(selectAddParamsSql, {'imei': imei})

#     if res:
#         id_taskart =  res[0]['id_taskart']
#         for i, elm in enumerate(res):
#             if not result:
#                 add_to_result(result)
#             else:
#                 if result[-1]['id_taskart'] == elm['id_taskart']:
#                     if result[-1]['add_params'][-1]['name_add'] == elm['name_add']:
#                         result[-1]['add_params'][-1]['vvalue'].append(elm['vvalue'])
#                     else:
#                         result[-1]['add_params'].append({
#                             'name_add': elm['name_add'], 'adddatatype': elm['adddatatype'],
#                             'vvalue': [elm['vvalue']], 'required': elm['required']
#                         })
#                 else:
#                     add_to_result(result)
#     return result
