# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .models import Article
from .models import MobileDevice
import json
from django.core import serializers
import hashlib
import uuid
import explore
import pricemon.settings as mySettings
import datetime
import logging
import base64
import os


# log = logging.getLogger('default')

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
		key = request.POST['key']
		querysetTasks = Task.objects.all()
		t_ids = []
		for t in querysetTasks:
			if t.mobileDevice.key == key:
				t_ids.append(t.id)

		querysetArts = Article.objects.filter(task_id__in=t_ids)
		jsonAr = {'articles': []}
		for article in querysetArts:
			begindate = article.task.begin_date.isoformat()
			enddate = article.task.end_date.isoformat()
			art = {
	            'task_name': article.task.name,
	            'id_task': article.task.id,
	            'enddate': enddate[8:10]+'.'+enddate[5:7]+'.'+enddate[0:4],
	            'begindate': begindate[8:10]+'.'+begindate[5:7]+'.'+begindate[0:4],
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
	            'ttp': article.task.tasktype,
	        }
			jsonAr['articles'].append(art)
		arts_list_json = json.dumps(jsonAr)
		# explore.stop()
		return HttpResponse(arts_list_json, 'application/javascript')
	else:
		return HttpResponse(str(dict({"error": "Wrong request"})), 'application/javascript')

@csrf_exempt
def login_mobile(request):
	if request.method == 'POST':
		uuid_m = request.POST['user']
		pw = request.POST['pw'] # todo hash
		queryset = MobileDevice.objects.filter(uuid=uuid_m)
		for q in queryset or []:
			md5pw = hashlib.md5(q.password).hexdigest()
			if pw == md5pw.upper():
				key = str(uuid.uuid1())
				q.key = key
				q.save()
				return HttpResponse(str(dict({"key": key})), 'application/javascript')
		return HttpResponse(str(dict({"error": "not authorized"})), 'application/javascript')
	else:
		return HttpResponse(str(dict({"error": "Wrong request"})), 'application/javascript')

@csrf_exempt
def set_tasks_mobile(request):
	if request.method == 'POST':
		if request.POST['param'] != "SetArts":
			return HttpResponse(str(dict({"error": "Wrong request"})), 'application/javascript')

		art_items = json.loads(request.POST['items'])
		date = datetime.datetime.now().isoformat()[0:10]
		storage_path = mySettings.PHOTO_STORAGE
		# explore.stop()

		for item in art_items:
			#Определяем параметры принимаемого задания
			try:
				p_performer = int(item.get('performer')) if (int(item.get('performer')) != -1) else None
			except:
				p_performer = None

			try:
				location_provider = int(item.get('location_provider')) if (int(item.get('location_provider')) != -1) else None
			except:
				location_provider = None

			try:
				p_price = float(item.get('price'))
			except:
				p_price = ''

			try:
				cur_date_time = None if item['cur_date_time'] == 'null' else item['cur_date_time'].replace('/', '.')
			except:
				cur_date_time = None

			try:
				p_latitude = float(item['lat'])
			except:
				p_latitude = None

			try:
				p_longitude = float(item['lng'])
			except:
				p_longitude = None

			try:
				quant = float(item['quant'])
			except:
				quant = None

			try:
				imei = item.get('imei') or None
			except:
				imei = None

			try:
				p_id_taskart = int(item.get('id_taskart')) or None
			except:
				p_id_taskart = None

			try:
				appVersion = item.get('appVersion') or None
			except:
				appVersion = None

			try:
				id_unit = item.get('id_unit') or None
			except:
				id_unit = None

			try:
				p_id_task = int(item.get('id_task')) or None
			except:
				p_id_task = None

			try:
				flag_exists = item.get('exists') or None
			except:
				flag_exists = None

			try:
				is_action = 1 if item.get('is_action') else None
			except:
				is_action = None


			#writing photo to storage
			if len(item["photo"]) > 10:
				photo_folder = os.path.join(storage_path, date, imei)
				if (not os.path.exists(photo_folder)):
					os.makedirs(photo_folder)
				photo_name = str(p_id_taskart) + '.jpg'
				photo_path = os.path.join(photo_folder, photo_name)

				photo_file = open(photo_path, 'w+')
				photo_file.write(base64.standard_b64decode(item['photo']))
				photo_file.close()

				relative_path = '/' + date + '/' + imei + '/' + photo_name
			else:
				relative_path = ''

				if not flag_exists:
					p_price = ''

			try:
				# writing to DB
				qs = Article.objects.get(id=p_id_taskart)
				qs.photo_path = relative_path
				qs.unit = id_unit
				qs.price = p_price
				qs.is_action = is_action
				qs.longitude = p_longitude
				qs.latitude = p_latitude
				qs.task.completedate = cur_date_time
				qs.save()
			except:
				return HttpResponse(str(dict({"error": "Error while sending the task"})), 'application/javascript')
		
		explore.stop()
		qs = Task.objects.get(id=p_id_task)
		qs.status = 1
		qs.save
		return HttpResponse(str(dict({"success": "true"})), 'application/javascript')

	else:
		return HttpResponse(str(dict({"error": "Wrong request"})), 'application/javascript')

	        # try:
	        #     if len(item.get('add_p')) > 10:
	        #         add_p = json.loads("[" + item["add_p"][1::][:-1].replace("[","{").replace("]","}").replace("'",'"') + "]")
	        #     else:
	        #         add_p = []
	        # except:
	        #     add_p = []
	        # log.error(add_p)
	        # sendAddParams(add_p, cur, p_id_taskart, p_id_task, imei)


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
		
# 		return HttpResponse(str(dict({"error": "not authorized"})), 'application/javascript')
# 	else:
# 		return HttpResponse(str(dict({"error": "Wrong request"})), 'application/javascript')
