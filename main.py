# encoding: utf-8
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import sys
import csv
import codecs

sys.setrecursionlimit(1000000)

host = 'https://sh.lianjia.com/zufang/'
uris = {'yangpu':'杨浦区','changning':'长宁区','songjiang':'松江区','jiading':'嘉定区','huangpu':'黄浦区','jingan':'静安区','zhabei':'闸北区','hongkou':'虹口区','qingpu':'青浦区','fengxian':'奉贤区','jinshan':'金山区','chongming':'崇明区','pudong/':'浦东区'}
pudongs =['ra1','ra2','ra3','ra4','ra5','ra6',]

def start():

    headers = ['标题', '小区名称','户型','面积','朝向','位置','楼层','小区建造时间','优点','价格','更新日期','查看人数']
    with open('lianjia.csv', 'w',) as f:
        # 标头在这里传入，作为第一行数据
        f.write('区\t标题\t小区名称\t户型\t面积\t朝向\t位置\t楼层\t小区建造时间\t优点\t价格\t更新日期\t查看人数\r\n')

    for uri in uris:
        if (uri =='pudong/'):
            for uri2 in pudongs:
                time.sleep(1)
                html = requests.get(host + uri + uri2).content
                district = uris[uri]
                paserData(html, district)
                pudongpaserNext(html,host + uri + uri2,district)
        else:
            time.sleep(1)
            html = requests.get(host+uri+'/pg'+'1').content
            district = uris[uri]
            paserData(html,district)
            paserNext(html,host+uri+'/pg',district)


def paserData(content,district):
    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all('div', attrs={'class': 'info-panel'})
    for item in items:
        # 查找标题
        title = item.find('h2')
        title = title.find('a')
        href = title['href']
        title = title.get_text()


        #小区名称
        name = item.find('span',attrs={'class':'region'})
        name = name.get_text()

        #户型
        structure = item.find('span', attrs={'class':'zone'})
        structure = structure.get_text()

        #面积
        size = item.find('span', attrs={'class': 'meters'})
        size = size.get_text()

        #朝向
        where = item.find('div', attrs={'class':'where'})
        spans = where.find_all('span')
        orientation = spans[4]
        orientation =  orientation.get_text()

        #位置
        other = item.find('div',attrs={'class':'other'})
        position = other.find('a')
        position = position.get_text()

        #楼层
        level = item.find('div', attrs={'class':'con'})
        strs = level.get_text().split('/')
        level =  strs[1]

        #小区建造时间
        buildtime = spans[1].get_text()
        buildtime = strs[2]


        #优点
        adv = item.find('div', attrs={'class': 'left agency'})
        adv = adv.get_text()

        #价格
        price=item.find('span',attrs={'class':'num'})
        price = price.get_text()

        # 更新日期
        updatetime=item.find('div',attrs={'class':'price-pre'})
        updatetime = updatetime.get_text()

        # 查看人数
        num = item.find('div', attrs={'class': 'square'})
        num = num.find('span')
        num = num.get_text()

        # headers = ['标题', '小区名称', '户型', '面积', '朝向', '位置', '楼层', '小区建造时间', '优点', '价格', '更新日期', '查看人数']
        # data = ['标题':title, '小区名称':name, '户型':structure, '面积':size, '朝向':orientation, '位置':position, '楼层':level, '小区建造时间':buildtime, '优点':adv, '价格':price, '更新日期':updatetime, '查看人数':num]
        # str =  "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\r\n" % (district,title,name,structure,size,orientation,position,level,buildtime,adv,price,updatetime,num)
        area = unicode(district, "utf8")
        str = area + '\t' + title + '\t' + name+ '\t' +structure + '\t' +size + '\t' +orientation + '\t' +position + '\t' + level + '\t' + buildtime + '\t' +adv + '\t' +price + '\t' +updatetime + '\t' + num + '\r\n'
        with open('lianjia.csv', 'a') as f:
             f.write(str.encode('utf8'))



def paserNext(content,host,district):
    soup = BeautifulSoup(content, 'html.parser')
    page  = soup.find('div',attrs={'comp-module':'page'})

    dic = page['page-data']
    dic = eval(dic)
    totalPage = dic['totalPage']
    curPage = dic['curPage']
    print district +'--' +'总数:' + str(totalPage) + '页  ' + '当前:' + str(curPage) + '页  '

    if curPage >= totalPage:
        return
    else:
        nextpagenum = curPage + 1
        nexturl = host + str(nextpagenum)
        time.sleep(1)
        html = requests.get(nexturl).content
        paserData(html, district)
        paserNext(html, host,district)

def pudongpaserNext(content,host,district):
    soup = BeautifulSoup(content, 'html.parser')
    page  = soup.find('div',attrs={'comp-module':'page'})
    dic = page['page-data']
    dic = eval(dic)
    totalPage = dic['totalPage']
    curPage = dic['curPage']
    print district + '--' + '总数:' + str(totalPage) + '页  ' + '当前:' + str(curPage) + '页  '


    if curPage >= totalPage:
        return
    else:
        nextpagenum = curPage + 1
        nexturl = host +'pg' +str(nextpagenum)
        time.sleep(1)
        html = requests.get(nexturl).content
        paserData(html, district)
        pudongpaserNext(html, host,district)

start()