import requests
from lxml import etree
import pandas as pd
from selenium import webdriver
import time
import os
class spider():
    def __init__(self):
        self.base_url = 'https://www.aqistudy.cn/historydata/'
        self.session = requests.session()
        self.cities = []
        self.city_list = []
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=option)
        self.browser.get('https://www.baidu.com/')#避免关闭标签时关闭浏览器
        self.homepage = self.browser.current_window_handle#获得主页的句柄
    def _get_cityurl(self,city_list = None):
        '''
        :param city_list: the list of city that you want to grab
        :return:city url
        '''
        if city_list is None:
            response = self.session.get(self.base_url)
            selector = etree.HTML(response.content)
            city_xpath = '//div[@class="all"]//div[@class="bottom"]//a//@href'
            self.cities = selector.xpath(city_xpath)
            '''
            for city in self.cities:
                self.cities_url.append(self.base_url+city)
            '''
        else:
            for c in city_list:
                self.cities.append('monthdata.php?city='+c)
    def get_month_data(self,city_list = None):
        '''
        :param city_list: the list of city that you want to grab.if param is none,grab all cities' weather
        :return:csv of each cities weather data
        '''
        self._get_cityurl(city_list)
        for city in self.cities:
            city_url = self.base_url+city
            city = city[19:]#获取城市名字
            self.city_list.append(city)
            self.browser.switch_to_window(self.homepage)
            new_window_url = 'window.open("{}")'.format(city_url)
            self.browser.execute_script(new_window_url)
            self.browser.switch_to_window(self.browser.window_handles[-1])
            title = self.browser.title
            try:
                time.sleep(2)
                result = self.browser.execute_script("return items")
                self.browser.close()
            except:
                print("获取失败,刷新后重新获取")
                self.browser.refresh()
                time.sleep(5)
                result = self.browser.execute_script("return items")
                self.browser.close()
            #保存数据
            if len(result) >0:
                for data in result:
                    data['city'] = city
                pd_data = pd.DataFrame(result)
                pd_data.to_csv('result/'+city+'.csv',index_label='index')
            print('获取{}天气数据完成'.format(city))

def mix_csv():
    p = 'result/'
    files = os.listdir(p)
    print("合并csv中。。。")
    df = pd.DataFrame()
    for path in files:
        try:
            f = open('result/'+path, 'r', encoding='utf-8')
        except:
            continue
        df2 = pd.read_csv(f, index_col='index')
        df = df.append(df2)
    df2 = df.sort_values(by=["city","time_point"], ascending=[True,True]).reset_index(drop=True)
    df2.to_csv('weather.csv', index_label='index')
    print('合并文件完成')

if __name__ == '__main__':
    if not os.path.exists('result'):
        os.mkdir('result')
    s = spider()
    s.get_month_data(['北京', '上海', '广州', '呼和浩特', '厦门', '武汉', '深圳', '杭州', '成都', '南京', '西安', '天津', '合肥', '乌鲁木齐', '海口', '南宁', '石家庄', '沈阳','哈尔滨','长春', '福州', '济南', '昆明', '兰州', '银川', '南昌', '郑州', '长沙', '贵阳', '西宁', '拉萨'])
    mix_csv()

