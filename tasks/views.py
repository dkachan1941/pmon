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
from scrapyd_api import ScrapydAPI


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
		    list.append({'name':row.name, 'competitor': row.competitor.name, 'price': row.price, 'group': "" if not row.group else row.group.name, 'unit': row.unit, 'photo': row.photo_path, 'quant': row.quant, 'latitude': row.latitude, 'longitude': row.longitude, 'is_action': row.is_action, 'manufacturer': row.manufacturer, 'quality': row.quality, 'weight': row.weight})
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
def run_spider(request):
	if request.method == 'POST':
		id_task = request.POST['id_task']
		sp_name = request.POST['sp_name'] # todo hash

		# explore.stop()
		qs = Task.objects.get(id=id_task)
		qs.in_work = True
		qs.save()

		scrapyd = ScrapydAPI('http://localhost:6800')
		# explore.stop()
		job_id = scrapyd.schedule('default', 'baucenter', id_task=id_task)
		return HttpResponse(json.dumps({"res": job_id}), 'application/javascript')
	else:
		return HttpResponse(json.dumps({"error": "error"}), 'application/javascript')

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

			try:
				manufacturer = item.get('manufacturer') or None
			except:
				manufacturer = None

			try:
				quality = item.get('quality') or None
			except:
				quality = None

			try:
				weight = item.get('weight') or None
			except:
				weight = None


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
				qs.quant = quant
				qs.longitude = p_longitude
				qs.latitude = p_latitude
				qs.manufacturer = manufacturer
				qs.quality = quality
				qs.weight = weight
				qs.task.completedate = cur_date_time
				qs.save()
			except:
				return HttpResponse(str(dict({"error": "Error while sending the task"})), 'application/javascript')

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



# @bpappsrv.route('/getaddparams', methods=['POST'])
# def getAdditionalParams():
#     log.info("The getAdditionalParams method in appserv have triggered")
#     # import explore
#     # explore.stop()
#     data = request.form
#     if not data:
#         return json.dumps({"error": "no addparams"})
#     if data.get('param') != 'GetAddParams' or not data.get('key'):
#         return json.dumps({'error' : 'No GetAddParams or key.'})

#     try:
#         additional_params = getAddParams(data.get('key'))
#         return json.dumps(additional_params)
#     except:
#         log.error('Error in GetAddParams.')
#         log.error(traceback.format_exc())
#         return json.dumps({'error' : 'Error in GetAddParams.'})



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



# def changepw():
#     log.info("The changepw method in appserv have triggered")
#     data = request.form
#     if not data:
#         return json.dumps({"error": "no data in changepw"})
    
#     if data.get('param') == 'ChangePw':
#         old_pw = data.get('pw_old')
#         new_pw = data.get('pw_new')
#         user = data.get('user')

#         con = model.db.connect()
#         cur = con.cursor()
#         pwSQL = """
#             Select cast(u.hashvalue as varchar2(32)) as pw
#             from CPMS.mobile_device u
#             where u.imei = hextoraw( :user)
#         """
#         res = cur.execute(pwSQL, {'user': user.decode('utf-8').encode('cp1251')})
#         old_password = '' if not len(res) else res[0]['pw']
#         if not old_password:
#             return json.dumps({"error": "You are not authorized"})

#         if old_password == old_pw:
#             res = cur.execute(sqls.changePwSql, {'new_pw': new_pw, 'user': user}, commit = True)
#             if not res:
#                 log.info("The user %s has changed password!" % user)
#                 return json.dumps({'success': 'true'})
#             else:
#                 log.info("The user %s tryed to change pw, but has no success, res: %s!" % (user, res))
#                 return json.dumps({'success': 'false'})
#         else:
#             return json.dumps({'error': 'wrong old password!'})
#     return json.dumps({'error' : 'Invalid user or password.'})



# def isAuthorized(context):
#     if hasattr(context.request.META.POST, 'read'):
#         data = json.loads(context.request.META.POST.read())
#     else:
#         data = context.request.META.POST
#         if hasattr(data, '__getitem__'):
#             if data.get('key'):
#                 key = data['key']
#                 # if key == 'CC6F3902140BCF40':
#                 #     data['user'] = key
#                 #     return data
#                 now = datetime.datetime.now()
#                 conn = sqlite3.connect(tango.SETTINGS.SQLITEDBPATH)
#                 cur = conn.cursor()
#                 mkeys = cur.execute('SELECT key, date_1, user FROM keys').fetchall()
#                 for u in mkeys:
#                     if key == u[0] and (now - datetime.datetime.strptime(u[1][0:19], '%Y-%m-%d %H:%M:%S')).seconds < tango.SETTINGS.SESSION_TIME:
#                         #если авторизация успешная, то продлим сессию
#                         cur.execute('UPDATE keys SET date_1 = ? WHERE key = ?', (now ,key))
#                         data['user'] = u[2]
#                         if tango.SETTINGS.LOGGING in ('max', 'min'):
#                             log.info('The user %s has required for a %s method' % (u[2], data.get('param')))
#                         conn.commit()
#                         conn.close()
#                         return data
#                 conn.commit()
#                 conn.close()
#             elif 'pw' in data:
#                 return data
#             elif data.get('param') == 'ChangePw':
#                 return data
#         return False


# def login(context):
#     try:
#         data = isAuthorized(context)
#         if data:
#             if hasattr(data, '__getitem__'):
#                 if data.get('param'):
#                     param = data['param']
#                     if tango.SETTINGS.LOGGING == 'max':
#                         log.info('The user %s has required for a %s method' % (data.get('user'), param))
#                     if param == 'Login':
#                         return check_login(data.get('user'), data.get('pw')) # вызываем процедуру логирования
#                     if param == 'ChangePw':
#                         return change_pw(data['user'], data['oldPw'], data['newPw']) # вызываем процедуру смены пароля
#             if tango.SETTINGS.LOGGING in ('max', 'min'):
#                 log.info('invalid request, data = %s' % data)
#             return str(dict({'error' : 'Invalid request. '}))
#         return str(dict({"error": "not authorized"}))
#     except IOError as e:
#         if e.errno == errno.EPIPE:
#             if tango.SETTINGS.LOGGING in ('max', 'min'):
#                 log.info('connection failed, error = %s' % str(e))
#             return str(dict({"error": "connection failed!"}))


# def check_login(user_in, pw_in): # возвращает ключ если пароль и логин правильные
#     if user_in and pw_in:
#         # explore.stop()
#         data = urllib.urlencode({'user': user_in, 'pw': pw_in})
#         try:
#             request = urllib2.Request(tango.SETTINGS.LOGINPATH, data)
#             response = urllib2.urlopen(request)
#             is_user_valid = int(response.read())
#             # print is_user_valid
#         except Exception as e:
#             if tango.SETTINGS.LOGGING in ('max', 'min'):
#                 log.info('check_login: DMZ Network error = %s' % str(e))
#             return str(dict({'error' : 'check_login: DMZ Network error. '}))

#         if is_user_valid:
#             key = str(uuid.uuid1())
#             conn = sqlite3.connect(tango.SETTINGS.SQLITEDBPATH)
#             cur = conn.cursor()
#             cur.execute('''CREATE TABLE if not exists keys (date_1 text, key text, user text)''')
#             now = datetime.datetime.now()

#             is_key_exists = cur.execute("SELECT 1 FROM keys WHERE user = ?", (user_in, )).fetchall()
#             if is_key_exists:
#                 cur.execute('UPDATE keys SET key = ?, date_1 = ? WHERE user = ?', (key, now, user_in))
#             else:
#                 cur.execute("INSERT INTO keys (date_1, key, user) VALUES (?,?,?)", (now, key, user_in))
#             conn.commit()
#             conn.close()

#             if tango.SETTINGS.LOGGING == 'max':
#                 log.info('The user %s got key = %s' % (user_in, key))
#             print str(dict({'key' : key}))
#             return str(dict({'key' : key}))
#         else:
#             # print str(dict({'error' : 'Invalid user or password. '}))
#             return str(dict({'error' : 'Invalid user or password. '}))
#     return str(dict({"error": "not authorized"}))


# def sendManifest(context):
#     if hasattr(context.request.META.POST, 'read'):
#         data = json.loads(context.request.META.POST)
#         if hasattr(data, '__getitem__'):
#             if data.get('user') and data.get('pw'):
#                 user = data['user']
#                 pw = data['pw']
#                 data = urllib.urlencode({'user': user, 'pw': pw})
#     if context.request.META.POST["user"]:
#         user = context.request.META.POST["user"]
#         data = urllib.urlencode({'user': context.request.META.POST["user"], 'pw': context.request.META.POST["pw"]})
#         try:
#             request = urllib2.Request(tango.SETTINGS.LOGINPATH, data)
#             response = urllib2.urlopen(request)
#         except Exception as e:
#             if tango.SETTINGS.LOGGING in ('max', 'min'):
#                 log.info('sendManifest: DMZ etwork error = %s' % str(e))
#             return str(dict({'error' : 'sendManifest: DMZ Network error. '}))
#         is_user_valid = int(response.read())
#         if is_user_valid:
#             try:
#                 json_data = open(os.path.join(tango.PROJECT_ROOT, tango.SETTINGS.MANIFESTPATH)).read()
#                 manifest = json.loads(json_data)
#                 if tango.SETTINGS.LOGGING == 'max':
#                     log.info('The user %s got manifest file' % user)
#                 return json.dumps(manifest)
#             except:
#                 if tango.SETTINGS.LOGGING in ('max', 'min'):
#                     log.error('The user %s got ERROR: no manifest file' % user)
#                 return str(dict({'error' : 'No manifest file. '}))
#         else:
#             return str(dict({'error' : 'Invalid username or password'}))
#     return str(dict({'error' : 'wrong request'}))

