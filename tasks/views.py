# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .models import Article
import json
from django.core import serializers
import hashlib

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
		uuid = request.POST['user']
		pw = request.POST['pw'] # todo hash
		queryset = mobileDevice.objects.filter(uuid=uuid)
		for q in queryset or []:
			md5pw = hashlib.md5(q.password).hexdigest()
			if md5pw == pw:
				print(md5pw)
				return HttpResponse('1', 'application/javascript')
		return HttpResponse('0', 'application/javascript')
	else:
		return json.dumps('{"error": "Wrong request"}')

@csrf_exempt
def set_tasks_mobile(request):
	pass

# 	data = request.form
#     if not data:
#         return json.dumps({"error": "no data in setarts"})
                
#     if data.get('param') != "SetArts":
#         return json.dumps({'error' : 'No SetArts.'})


#     # explore.stop()
        
#     art_items = json.loads(data.get('items'))
#     mwIds = json.loads(data.get('mwIds'))
#     con = model.db.connect()
#     cur = con.cursor()
        
#     clearArtsTable = True
        
#     storage_path = current_app.config.get('PHOTO_DIR')
#     date = datetime.datetime.now().isoformat()[0:10]

#     for item in art_items:
#         #Определяем все параметры принимаемого задания
#         try:
#             photob64 = cx_Oracle.Binary(base64.standard_b64decode(item['photo']))
#             photob64_in = cur.var(cx_Oracle.BLOB)
#             photob64_in.setvalue(0,photob64)
#         except:
#             photob64_in = cx_Oracle.Binary('')
            
#         try:
#             p_performer = int(item.get('performer')) if (int(item.get('performer')) != -1) else None
#         except:
#             p_performer = None
    
#         try:
#             location_provider = int(item.get('location_provider')) if (int(item.get('location_provider')) != -1) else None
#         except:
#             location_provider = None

#         try:
#             p_price = float(item.get('price'))
#         except:
#             p_price = ''
    
#         try:
#             cur_date_time = None if item['cur_date_time'] == 'null' else item['cur_date_time'].replace('/', '.')
#         except:
#             cur_date_time = None
        
#         try:
#             p_latitude = float(item['lat'])
#         except:
#             p_latitude = None

#         try:
#             p_longitude = float(item['lng'])
#         except:
#             p_longitude = None

#         try:
#             quant = float(item['quant'])
#         except:
#             quant = None

#         try:
#             pricefrom1 = float(item['pricefrom1'])
#         except:
#             pricefrom1 = None

#         try:
#             priceto1 = float(item['priceto1'])
#         except:
#             priceto1 = None

#         imei = item.get('imei') or None

#         # очистим временную таблицу в БД с т.п.
#         if clearArtsTable:
#             logCallproc(cur, 'cpms.clear_taskart_device_valid_prc', [imei])
#             clearArtsTable = False

#         p_id_taskart = int(item.get('id_taskart')) or None
#         appVersion = item.get('appVersion') or None
#         id_unit = item.get('id_unit') or None
#         p_id_task = int(item.get('id_task')) or None
#         flag_exists = item.get('exists') or None
#         is_action = 1 if item.get('is_action') else None

#         #writing photo to storage
#         if len(item["photo"]) > 10:
#     <-->    #log.error('photo id_taskart = ' + str(p_id_taskart)) # debug
#     <-->    try:
#                 photo_folder = os.path.join(storage_path, date, imei)
#                 if (not os.path.exists(photo_folder)):
#                     os.makedirs(photo_folder)
#                 photo_name = str(p_id_taskart) + '.jpg'
#                 photo_path = os.path.join(photo_folder, photo_name)
                
#                 photo_file = open(photo_path, 'w+')
#                 photo_file.write(base64.standard_b64decode(item['photo']))
#                 photo_file.close()
                
#                 relative_path = '/' + date + '/' + imei + '/' + photo_name
#                 log.info('relative_path = ' + relative_path)
#     <-->    except:
#                 log.error('error: cannot write file') # debug
#     <--><------>#sys.exc_info()[0]
#         else:
#             relative_path = ''
                
#         if 'id_task' in item:
#             log.info("The user %s is sending the task id = %s" % (imei, p_id_task))
            
#         # Отправляем задания типа "Постоянный шаблон"
#         if item.get('ttp') in ['mw', 'mwd']:
#             res = '00'
#             try:
#                 res = logCallproc(cur, 'CPMS.update_task_art', [p_id_taskart, p_price, p_latitude, p_longitude, relative_path, quant, id_unit, is_action, cur_date_time, appVersion, imei, pricefr
#             except:
#                 return json.dumps({"error": "Error while sending the task"})
#             if (res == None):
#                 return json.dumps({"error": "Error while sending the task"})
#             log.info("The user %s sent the task id = %s; commited!" % (imei, p_id_task))
#             log.error("res = " + str(res))

#         else:
#             if not flag_exists:
#                 p_price = ''

#             # explore.stop()


# <------>    log.error("id_tasksart = " + str(p_id_taskart))
# <------>    log.error("p_price = " + str(p_price))
# <------>    log.error("p_latitude = " + str(p_latitude))
# <------>    log.error("p_longitude = " + str(p_longitude))
# <------>    log.error("cur_date_time = " + str(cur_date_time))
#             log.error("location_provider = " + str(location_provider))
#             res = '00'
#             try:
#                 res = logCallproc(cur, 'CPMS.update_task_art', [p_id_taskart, p_price, p_latitude, p_longitude, relative_path,quant, id_unit, is_action, cur_date_time, appVersion, imei, pricefro
#             except:
#                 return json.dumps({"error": "Error while sending the task"})
#             if (res == None):
#                 return json.dumps({"error": "Error while sending the task"})
#             log.info("The user %s sent the task id = %s; commited!" % (imei, p_id_task))
#             log.error("res = " + str(res))
            
#         # Отправляем все доп.параметры - нужно для заданий всех типов
#         #log.error("item.get('add_p')")
#         #log.error(item.get('add_p'))
#         #log.error(len(item.get('add_p')) > 10)
#         try:
#             if len(item.get('add_p')) > 10:
#                 add_p = json.loads("[" + item["add_p"][1::][:-1].replace("[","{").replace("]","}").replace("'",'"') + "]")
#                 # add_p = json.loads(item['add_p']) if item.get('add_p') else None
#             else:
#                 add_p = []
#         except:
#             add_p = []
#         log.error(add_p)
#         sendAddParams(add_p, cur, p_id_taskart, p_id_task, imei)
#     cur.execute("commit")


#     #Let's check now whether everyting sent or not
#     sqlGetArtsForSend = """select id_taskart
#                               from cpms.taskart_device_valid_vw
#                              where imei = :p_imei"""
#     if len(art_items):
#         res = cur.execute(sqlGetArtsForSend, {'p_imei': art_items[0].get('imei')})
#     #log.error("len art_items = " + str(len(art_items)))
# <------>if len(res) == 0:
#     <-->    if len(mwIds):
#         <------>for id_mwtask in mwIds:
#             <-->    logCallproc(cur, 'cpms.create_copy_task_prc', [int(id_mwtask)])
#             <-->    cur.execute("commit")
#             <-->    log.error("debug: create_copy_task_prc with id_task = %s " % (id_mwtask))

#         return '1'
#     else:
#         return json.dumps({"error": "some arts left"})



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
