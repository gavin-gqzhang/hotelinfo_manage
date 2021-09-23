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
from django.urls import path

from hotel import views
from django.conf.urls import url

app_name = 'hotel'

urlpatterns = [
    # 页面渲染相关路由

    # --------------------
    # 酒店后台登录
    url(r'^login/$', views.index, name='index'),
    # 酒店注册
    url(r'^regist/$', views.regist, name='regist'),
    # 验证码
    url(r'^ver_code', views.verification, name='ver_code'),
    # 酒店后台首页
    url(r'^index/$', views.backstage_index, name='backstage_index'),
    # 修改密码页面渲染
    # url(r'change/$', views.backstage_change, name='backstage_change'),
    # 订单列表
    url(r'order_list/$', views.order_list, name='order_list'),
    # 用户信息列表
    url(r'^user_list/$', views.user_list, name='user_list'),
    # 订单详情页面渲染
    path('order_datail/<str:order_num>', views.order_datail, name='order_datail'),
    # 酒店信息页面渲染
    url(r'^hotel_info/$', views.hotel_info, name='hotel_info'),
    # 个人信息页面渲染
    url(r'^user_info/$', views.user_info, name='user_info'),
    # 房间信息渲染
    url(r'^home_info/$', views.home_info, name='home_info'),
    # 全部收益信息页面渲染
    url(r'^sale_info/$',views.sale_info,name='sale_info'),
    # 员工工资信息页面渲染
    url(r'^staff_pay/$',views.staff_pay,name='staff_pay'),
    # 员工首页信息渲染
    url(r'staff_index/$',views.staff_index,name='staff_index'),
    # 房屋清洁信息渲染
    url(r'^home_clean_info/$', views.home_clean_info, name='home_clean_info'),
    # 个人工资信息渲染
    url(r'^staff_wage/$',views.staff_wage,name='staff_wage'),
    # 后端逻辑处理

    # ----------------------
    # 登录信息提交
    url('^merchants_login/$', views.merchants_login, name='merchants_login'),
    # 注册信息提交
    url(r'^becom_merchants/$', views.becom_merchants, name='becom_merchants'),
    # 修改个人信息提交
    url(r'^update_staff_info/$', views.update_staff_info, name='update_staff_info'),
    # 修改酒店信息
    url(r'^submit_hotel_info',views.submit_hotel_info,name='submit_hotel_info'),
    # 修改房型信息
    url(r'^update_hometype/$',views.update_hometype,name='update_hometype'),
    # 修改房间信息
    url(r'^update_homenum/$',views.update_homenum,name='update_homenum'),
    # 添加房型
    url(r'^add_hometype/$',views.addhometype,name='add_hometype'),
    # 添加房间信息
    url(r'^add_homenum/$',views.addhomenum,name='add_homenum'),
    # 修改个人信息
    url(r'^update_userinfo/$',views.update_userinfo,name='update_userinfo'),
    # 添加员工信息
    url(r'^add_staff/$',views.add_staff,name='add_staff'),
    # 房态变更
    path('clean_home/<str:home_num>/',views.clean_home,name='clean_home'),
]
