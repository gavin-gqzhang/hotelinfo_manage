# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 15:54
# @contact : puppet_life@163.com
# @Author  : puppet
# @Site    : 用于非视图外的方法的创建
# @File    : function.py
# @Software: PyCharm
import calendar
import hashlib
import json
import os
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from math import sin, radians, fabs, cos, asin, sqrt
from smtplib import SMTP_SSL
from urllib import parse
import requests
import matplotlib
import matplotlib.pyplot

# 发送邮件
from django.utils import timezone


def send_mail(option,message):
    """
        sender_qq:发送者的qq
        pwd：SMTP服务的密码，在qq邮箱中打开SMTP服务将密码修改
        send_mail:发送者邮箱
        receivers：接收者邮箱
    """
    host_server = 'smtp.qq.com'
    sender_qq = '2230685848'
    pwd = 'jiogkssbuptddifc'
    send_mail = '2230685848@qq.com'
    receivers = '2230685848@qq.com'
    # 确定操作，修改密码进行邮箱验证
    if option=="修改密码":
        mail_content="""
        <h1>验证邮箱</h1>
        <h3>您的账户正在申请重置密码，如果是本人操作请点击以下链接完成邮箱验证</h3>
        <br>
        <hr/>
        <a href="{0}">邮箱验证，点击修改密码</a>
        <hr/>
        <p>感谢您使用本系统，未来我们将会不断优化，给您最好的用户体验</p>
        """.format("127.0.0.1:8000/email/"+message['reset_code'])
        mail_title="确认邮箱"
    else:
        mail_content=""
        mail_title=""

    try:
        smtp=SMTP_SSL(host_server)
        smtp.ehlo(host_server)
        smtp.login(sender_qq,pwd)

        msg=MIMEText(mail_content,'html','utf-8')
        msg['Subject'] = Header(mail_title, 'utf-8')
        msg['From'] = send_mail
        msg['To'] = receivers
        smtp.sendmail(send_mail, receivers, msg.as_string())
        smtp.quit()
    except:
        print('邮件无法发送，出现错误')

#    两点键位置信息具体测定   #
EARTH_RADIUS = 6371  # 地球平均半径，6371km
#      对输入的两个经纬度信息进行测距   #
def hav(theta):
    s = sin(theta / 2)
    return s * s
def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance
#     获取详细地址的经纬度信息函数        #
def address(address):
    address_index = {}
    queryStr = '/geocoder/v2/?address=%s&output=json&ak=leDOPGBU5Gwk6D3wGZigrNk560zN50GX' % address
    encodeStr = parse.quote(queryStr, safe="/:=&?#+!$,;@'()*[]")
    rawStr = encodeStr + 'leDOPGBU5Gwk6D3wGZigrNk560zN50GX'
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    res = requests.get(url)
    json_data = json.loads(res.text)
    longitude = json_data['result']['location']['lng']  # 经度
    latitude = json_data['result']['location']['lat']  # 纬度
    address_index['lng'] = longitude
    address_index['lat'] = latitude
    return address_index  # 返回携带具体经纬度信息的字典

# 获取未来七天的时间
def get_time():
    time=timezone.localdate()
    year = time.strftime('%Y')
    mouth=time.strftime('%m')
    day=time.strftime('%d')
    times=[]
    times.append(datetime(year=int(year),month=int(mouth),day=int(day)).strftime('%Y-%m-%d'))
    for i in range(1,8):
        if int(day)+1>int(calendar.monthrange(int(year),int(mouth))[1]) and int(mouth)+1!=13:
            day=1
            mouth=int(mouth)+1
            now=datetime(year=int(year),month=mouth,day=day)
        elif int(day)+1>int(calendar.monthrange(int(year),int(mouth))[1]) and mouth+1==13:
            day=1
            mouth=1
            year=int(year)+1
            now=datetime(year=year,month=mouth,day=day)
        else:
            day=int(day)+1
            now=datetime(year=int(year),month=int(mouth),day=int(day))
        now = now.strftime('%Y-%m-%d')
        times.append(now)

    return times

# 获取过去七天时间
def get_last_time(date):
    year=str(date).split('-')[0]
    month=str(date).split('-')[1]
    day=str(date).split('-')[2]
    times=[]
    for i in range(1,8):
        if int(day)-1!=0:
            day=int(day)-1
            days=datetime(year=int(year),month=int(month),day=int(day))
        elif int(day)-1==0 and int(month)-1!=0:
            month=int(month) - 1
            day=int(calendar.monthrange(int(year),int(month))[1])
            days=datetime(year=int(year),month=month,day=int(day))
        else:
            month=12
            year=int(year)-1
            day=int(calendar.monthrange(int(year),int(month))[1])
            days=datetime(year=int(year),month=int(month),day=int(day))
        days=days.strftime('%Y-%m-%d')
        times.append(days)
    return times



def get_out_time(time,data):
    year = str(time).split('-')[0]
    mouth=str(time).split('-')[1]
    day=str(time).split('-')[2]
    for i in range(int(data)):
        if int(day)+1>int(calendar.monthrange(int(year),int(mouth))[1]) and int(mouth)+1!=13:
            day=1
            mouth=int(mouth)+1
            now=datetime(year=int(year),month=mouth,day=day)
        elif int(day)+1>int(calendar.monthrange(int(year),int(mouth))[1]) and mouth+1==13:
            day=1
            mouth=1
            year=int(year)+1
            now=datetime(year=year,month=mouth,day=day)
        else:
            day=int(day)+1
            now=datetime(year=int(year),month=int(mouth),day=int(day))
        now = now.strftime('%Y-%m-%d')

    return now

# 获取今日的剩余时间，半个小时为一截
def get_minute():
    time=timezone.localtime()
    hour=time.strftime('%H')
    minute=time.strftime('%M')
    times=[]
    for i in range(48):
        if i==0:
            if int(minute)<=30:
                now=("{}:{} - {}:{}".format(int(hour),30,int(hour)+1,'00'))
            else:
                now=("{}:{} - {}:{}".format(int(hour)+1,'00',int(hour)+1,30))
            hour=int(hour)+1
        if int(hour)==24 and i!=0:
            break
        if int(hour)!=24 and i!=0:
            now = ("{}:{} - {}:{}".format((hour - 1), 30, hour, '00'))
            times.append(now)
            if int(minute)<=30:
                now=("{}:{} - {}:{}".format(int(hour),30,int(hour)+1,'00'))
            else:
                now=("{}:{} - {}:{}".format(int(hour),'00',int(hour),30))
            # times.append(now)
        hour=int(hour)+1
        times.append(now)

    return times

# 画图
def pint(x,x_label,y,y_label,label,title,hotel_name):
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    plt=matplotlib.pyplot
    plt.plot(x,y,label=label,marker='o',color='r')
    # 图例生效
    plt.ylim(0,)
    plt.legend()
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    url='media/{}'.format(hotel_name)
    if not os.path.exists(url):
        os.makedirs(url)
    url=url+'/{}.jpg'.format(title)
    plt.savefig(url)
    return hotel_name+'/{}.jpg'.format(title)