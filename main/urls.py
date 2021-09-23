"""hotelinfo_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    # 页面渲染相关路由

    # ----------------
    # 首页路由
    url(r'^index/$', views.index, name='index'),
    # 用户的登录
    url(r'^sign_in/$', views.login, name='login'),
    # 用户注册
    url(r'^sign_up/$', views.regist, name='regist'),
    # 重置密码
    url(r'^forget_password/$', views.reset_password, name='reset_password'),
    # 验证码
    url(r'^ver_code', views.verification, name='ver_code'),
    # 个人首页
    url(r'^home/$', views.my_home, name='home'),
    # 个人订单列表
    url(r'^order_list/$',views.order_list,name='order_list'),
    # 酒店列表罗列
    url(r'^hotel_list/$', views.hotel_list, name='hotel_list'),
    # 酒店详细信息
    path('hotel_datail/<str:hotel_name>/',views.hotel_datail,name='hotel_datail'),
    # 确认订单页面渲染
    path('order/<int:hotel_id>/<int:home_id>',views.order_page,name='oder_page'),
    # 订单详情
    path('order_datail/<str:order_num>/',views.order_datail,name='order_datail'),
    # 用户登陆后修改密码页面渲染
    url(r'^mybackage_reset_password/$',views.my_home_reset_password,name='my_home_reset_password'),
    # 退出登录
    url(r'^sign_out/$',views.sign_out,name='sign_out'),

    # 页面逻辑请求处理路由

    # ----------------
    # 登录验证
    url(r'^login_ver/$', views.login_ver, name='login_ver'),
    # 注册验证
    url(r'^regist_ver/$', views.regist_ver, name='regist_ver'),
    # 重置密码验证
    url(r'^reset_ver/$', views.reset_ver, name='reset_ver'),
    # 确认邮箱并进行密码修改路由
    path('email/<reset_code>/', views.make_sure_email, name='make_sure_email'),
    # 修改密码确认
    url(r'^reset_password/$', views.change_password, name='change_password'),
    # 酒店信息搜索 通过距离
    url(r'^search_by_distance/$', views.search_by_distance, name='search_by_distance'),
    # 酒店信息搜索 通过名称
    url(r'^search_by_name/$', views.search_by_name, name='search_by_name'),
    # 修改个人信息
    url(r'^change_info/$',views.change_info,name='change_info'),
    # 酒店确认入住并分配房间信息
    path('to_stay_in/<str:order_num>/',views.to_stay_in,name='to_stay_in'),
    # 提交订单
    url(r'^submit_order/$',views.submit_order,name='submit_order'),
    # 订单确认成功并入住
    url(r'^order_sure/$',views.order_sure,name='order_sure'),

]
