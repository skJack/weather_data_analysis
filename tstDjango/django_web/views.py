from django.shortcuts import render
from django_web.models import ItemInfo
#from models import ItemInfo
# Create your views here.
cities_list = ['北京', '上海', '广州', '呼和浩特', '厦门', '武汉', '深圳', '杭州', '成都', '南京', '西安', '天津', '合肥', '乌鲁木齐', '海口', '南宁', '石家庄','沈阳','哈尔滨','长春', '福州', '济南', '昆明', '兰州', '银川', '南昌', '郑州', '长沙', '贵阳', '西宁', '拉萨']
def index(requset):
    list = []
    for i in range(4):
        city_list = []
        seriers = [i for i in get_info_year(i)]
        date = 1  # 月份变量
        for serier in seriers:
            tmp = []
            tmp.append(date)
            tmp.append(serier['aqi'])
            tmp.append(serier['maxaqi'])
            tmp.append(serier['pm25'])
            tmp.append(serier['O3'])
            tmp.append(serier['quality'])
            city_list.append(tmp)
            date = date + 1
        list.append(city_list)
    seriers_bj = [i for i in get_info(1)]
    seriers_sjz = [i for i in get_info(0)]
    seriers_hhht = [i for i in get_info(2)]
    aqi_list_bj = [i['aqi'] for i in seriers_bj]
    aqi_list_sjz = [i['aqi'] for i in seriers_sjz]
    aqi_list_hhht = [i['aqi'] for i in seriers_hhht]
    pm_list_bj = [i['pm2.5'] for i in seriers_bj]
    pm_list_sjz = [i['pm2.5'] for i in seriers_sjz]
    pm_list_hhht = [i['pm2.5'] for i in seriers_hhht]
    so2_list_bj = [i['SO2'] for i in seriers_bj]
    so2_list_sjz = [i['SO2'] for i in seriers_sjz]
    so2_list_hhht = [i['SO2'] for i in seriers_hhht]
    context = {
        'aqi_BJ': aqi_list_bj,
        'aqi_SJZ': aqi_list_sjz,
        'aqi_HHHT': aqi_list_hhht,
        'pm25_BJ': pm_list_bj,
        'pm25_SJZ': pm_list_sjz,
        'pm25_HHHT': pm_list_hhht,
        'so2_BJ':so2_list_bj,
        'so2_SJZ':so2_list_sjz,
        'so2_HHHT':so2_list_hhht
    }
    list.append(context)
    return render(requset,'index.html',{'result_list':list})


def chart(request):
    return render(request,'chart2.html')
def chart2(request):
    return render(request, 'chart.html')
def index_data(requset):
    return render(requset,'index_data.html')
def tables(request):
    return render(request, 'tables.html')
def get_info(city_index):
    '''
    用于柱状图
    :param city_index: 城市索引
    '''
    pipeline_sjz = [
        {'$match': {
            '$and': [{'$or': [{'Time': '2019-01'}, {'Time': '2018-01'}, {'Time': '2017-01'}]}, {'City': '石家庄'}]}}
    ]
    pipeline_bj = [
        {'$match': {
            '$and': [{'$or':[{'Time': '2019-01'}, {'Time': '2018-01'}, {'Time': '2017-01'}]}, {'City': '北京'}]}},
    ]
    pipeline_hhht = [
        {'$match': {
            '$and': [{'$or':[{'Time': '2019-01'}, {'Time': '2018-01'}, {'Time': '2017-01'}]}, {'City': '呼和浩特'}]}},
    ]
    if(city_index==1):
        choose=pipeline_bj
        #city='北京'
    elif(city_index==0):
        choose=pipeline_sjz
        # city='石家庄'
    elif(city_index==2):
        choose=pipeline_hhht
    for i in ItemInfo._get_collection().aggregate(choose):
        date_={
            'name':i['City'],
            'aqi':i['AQI'],
            'pm2.5':i['PM25'],
            'SO2':i['SO2']
        }
        yield date_
def get_info_new(city_index):
    '''
    用于地图显示
    :param city_index: 城市索引
    '''
    pipeline = [
        {
            '$match': {
                '$and': [
                    {'Time': '2019-01'},{'City': cities_list[city_index]}]}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data_ = {
            'name':i['City'],
            'aqi':i['AQI'],
            'quality':i['Quality'],
            'pm25':i['PM25']
        }
        yield data_
def get_info_year(city_index):
    '''
    获得一年的城市数据，用于散点图显示
    :param city_index: 城市索引
    '''
    pipeline = [
        {'$match': {
            '$and': [{'$or': [{'Time': '2018-01'}, {'Time': '2018-02'}, {'Time': '2018-03'},{'Time': '2018-04'},{'Time': '2018-05'},{'Time': '2018-06'},
                              {'Time': '2018-07'},{'Time': '2018-08'},{'Time': '2018-09'},{'Time': '2018-10'},{'Time': '2018-11'},{'Time': '2018-12'}]},
                     {'City': cities_list[city_index]}]}},
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data_ = {
            'name': i['City'],
            'aqi': i['AQI'],
            'quality': i['Quality'],
            'pm25':i['PM25'],
            'SO2':i['SO2'],
            'O3':i['O3'],
            'maxaqi':i['MaxAQI'],
            'time':i['Time'],
            'quality':i['Quality']
        }
        yield data_


def slatter(request):
    list = []
    for i in range(4):
        city_list = []
        seriers = [i for i in get_info_year(i)]
        date = 1#月份变量
        for serier in seriers:
            tmp = []
            tmp.append(date)
            tmp.append(serier['aqi'])
            tmp.append(serier['maxaqi'])
            tmp.append(serier['pm25'])
            tmp.append(serier['O3'])
            tmp.append(serier['quality'])
            city_list.append(tmp)
            date = date + 1
        list.append(city_list)
    return render(request,'slatter.html',{'result_list':list})



def chart(request):
    seriers_bj = [i for i in get_info(1)]
    seriers_sjz = [i for i in get_info(0)]
    seriers_hhht = [i for i in get_info(2)]
    aqi_list_bj = [i['aqi'] for i in seriers_bj]
    aqi_list_sjz = [i['aqi'] for i in seriers_sjz]
    aqi_list_hhht = [i['aqi'] for i in seriers_hhht]
    pm_list_bj = [i['pm2.5'] for i in seriers_bj]
    pm_list_sjz = [i['pm2.5'] for i in seriers_sjz]
    pm_list_hhht = [i['pm2.5'] for i in seriers_hhht]
    context={
        'aqi_BJ':aqi_list_bj,
        'aqi_SJZ':aqi_list_sjz,
        'aqi_HHHT':aqi_list_hhht,
        'pm25_BJ':pm_list_bj,
        'pm25_SJZ':pm_list_sjz,
        'pm25_HHHT':pm_list_hhht
    }
    return render(request,'chart2.html',{'result_list':context})

def map(request):
    result_dict = {}
    for i in range(len(cities_list)):
        seriers = [j for j in get_info_new(i)]
        result_dict[seriers[0]['name']] = seriers[0]['aqi']
    return render(request,'map.html',{'result_list':result_dict})

def tables(request):
    list = []
    for i in range(10):
        seriers = [j for j in get_info_new(i)]
        list.append(seriers[0]['pm25'])
    return render(request,'tables.html',{'result_list':list})
def charts(request):
    return render(request,'charts.html')