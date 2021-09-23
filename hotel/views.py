import random
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from main.function import *
from main.models import *

# Create hotel views here.


# 酒店后台登录页面渲染
def index(request):
    return render(request,'hotel/login.html')

# 酒店后台注册页面渲染
def regist(request):
    return render(request,'hotel/registration.html')

# 酒店后台首页渲染
def backstage_index(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    if user.is_staff==1:
        return render(request,'hotel/index.html',context={'is_staff':1})
    order_list=Order.objects.filter(hotelid=user.hotel_id)
    staff_list=AuthUser.objects.filter(hotel_id=user.hotel_id)
    home_list=HomeInfo.objects.filter(hotelid=user.hotel_id)
    today_order_price=0
    total_order_price=0
    total_order=len(order_list)
    today_order=0
    today=timezone.localdate()
    # 计算今天和全部的销售总额
    for order in order_list:
        total_order_price=float(total_order_price)+float(order.price)
        detail_time=order.ordertime.strftime('%Y-%m-%d')
        if str(detail_time)==str(today):
            today_order_price=float(today_order_price)+float(order.price)
            today_order=int(today_order)+1
    user_info_list=[]
    for staff in staff_list:
        user_info_list.append(Userinfo.objects.get(id=staff.user_id))
    # 计算已住房间数目
    for home in home_list:
        is_live_num=0
        home_nums=HomeNum.objects.filter(hotelid=user.hotel_id,homeid=home.id)
        for home_num in home_nums:
            if home_num.is_live==1:
                is_live_num=int(is_live_num)+1
        # home_live_num.append(is_live_num)
        home.live_num=is_live_num
        home.live_rate=float(int(is_live_num)/int(home.num))*100
        home.save()

    context={
        'today_order_price':today_order_price,
        'total_order_price':total_order_price,
        'total_order':total_order,
        'today_order':today_order,
        'order_list':order_list,
        'staff_list':user_info_list,
        'home_list':home_list,
        'local_time':timezone.localdate(),
    }
    return render(request,'hotel/index.html',context=context)

# 酒店后台用户信息页面渲染
def user_info(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    if user.is_staff==1:
        return render(request,'hotel/index.html',context={'is_staff':1})
    userinfo=Userinfo.objects.get(id=user.user_id)
    context={
        "username":username,
        "name":userinfo.name,
        "email":user.email,
        "phone":userinfo.phone,
        "qq":userinfo.qq,
        "hotel_name":HotelInfo.objects.get(id=user.hotel_id).name,
        "create_date":user.date_joined,
        "last_login":user.last_login,
    }
    return render(request,'hotel/user-info.html',context=context)

# 酒店信息页面渲染
def hotel_info(request):
    if request.session.get('username'):
        username=request.session.get('username')
        try:
            user=AuthUser.objects.get(username=username)
            if user.is_staff == 1:
                return render(request, 'hotel/index.html', context={'is_staff': 1})
            hotel=HotelInfo.objects.get(id=user.id)
            user_info=Userinfo.objects.get(id=user.user_id)
            context={
                'username':username,
                'name':user_info.name,
                'email':user.email,
                'phone':user_info.phone,
                'address':hotel.address,
                'hotel_name':hotel.name,
                'hotel_phone':hotel.phone,
                'hotel_opentime':hotel.open_time,
                'hotel_detail':hotel.detail,
                'hotel_city':hotel.city,
            }
            return render(request,'hotel/hotel-info.html',context=context)
        except Userinfo.DoesNotExist:
            user_info=Userinfo(
                name="".join(i for i in random.sample("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890",random.randint(5,40)))
            )
            user_info.save()
            context = {
                'username': username,
                'name': user_info.name,
                'email': user.email,
                'phone': user_info.phone,
                'address': hotel.address,
                'hotel_name': hotel.name,
                'hotel_phone': hotel.phone,
                'hotel_opentime': hotel.open_time,
                'hotel_detail': hotel.detail,
                'hotel_city': hotel.city,
            }
            return render(request, 'hotel/hotel-info.html', context=context)
        except  AuthUser.DoesNotExist:
            request.session.flush()
            return render(request,'hotel/registration.html',context={"msg":"未查找到该用户，请注册后登录"})
        except  HotelInfo.DoesNotExist:
            request.session.flush()
            return render(request,'hotel/registration.html',context={"msg":"未查找到该酒店，请注册后登录"})
    else:
        return redirect(reverse('hotel:index'))

# 酒店房型信息页面渲染
def home_info(request):
    if not request.session.get('username'):
        return redirect(reverse('hotel:index'))
    else:
        username=request.session.get('username')
        user=AuthUser.objects.get(username=username)
        if user.is_staff == 1:
            return render(request, 'hotel/index.html', context={'is_staff': 1})
        hotel_id=HotelInfo.objects.get(id=user.hotel_id).id
        home_list=HomeInfo.objects.filter(hotelid=hotel_id)
        home_num_list=HomeNum.objects.filter(hotelid=hotel_id)
        user_list=AuthUser.objects.filter(hotel_id=user.hotel_id)
        name=[]
        for i in user_list:
            name.append(Userinfo.objects.get(id=i.user_id).name)
        context={
            'home_list':home_list,
            'home_nums':home_num_list,
            'user_list':name
        }
        return render(request,'hotel/home-info.html',context=context)

# 酒店后台修改密码页面
# def backstage_change(request):
#     return None

# 订单列表页面渲染
def order_list(request):
    # 首先判断登录状态，通过session判断
    if not request.session.get('username'):
        # 使用的是反向路由解析，重定位至登录页面，其中session.get是获取到输入的username的值，这个是在登录的时候创建的
        return redirect(reverse('main:login'))
    # 如果已经成功登录，下面开始进行数据获取
    # 首先我们看到如果获取订单的话，是需要匹配酒店的id，也就是hotelid
    # 如果获取酒店的id，我们需要对当前登录的账户进行获取详细信息，首先先获取session中存储的username的值
    username=request.session.get('username')
    if AuthUser.objects.get(username=username).is_staff==1:
        return render(request,'hotel/index.html',context={'is_staff':1})
    # authuser是模型类，其对应的是我们的数据库表，其下面有列名，可以直接使用.进行对应列名的信息获取
    # get是匹配单条数据，filter是 匹配多条数据
    hotelid=AuthUser.objects.get(username=username).hotel_id
    order_list=Order.objects.filter(hotelid=hotelid)
    # 我们可以看到还有homeid即房间类型id，需要进行房间类型的匹配
    # 获取全部的房间类型
    home_list=HomeInfo.objects.filter(hotelid=hotelid)
    # 创建一个字典，把我们要传递到前端的内容放入字典中
    context={
        'order_list':order_list,
        'home_list':home_list,
    }
    # 进行页面的渲染，同时向前端页面传递数据，右侧是我已经写好的HTML页面，下面我直接演示如何讲我们传递的字典信息内容渲染到前端页面
    return render(request, 'hotel/order_list.html',context=context)

# 用户列表渲染
def user_list(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    if user.is_staff==1:
        return render(request,'hotel/index.html',context={'is_staff':1})
    userlist=AuthUser.objects.filter(hotel_id=user.hotel_id)
    homelist=HomeInfo.objects.filter(hotelid=user.hotel_id)
    homenums=HomeNum.objects.filter(hotelid=user.hotel_id)
    users=[]
    for i in userlist:
        users.append(Userinfo.objects.get(id=i.user_id))
    context={
        'userlist':users,
        'homelist':homelist,
        'homenums':homenums
    }
    return render(request, 'hotel/user_list.html',context=context)

# 订单详情页面渲染
def order_datail(request,order_num):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    if AuthUser.objects.get(username=username).is_staff==1:
        return render(request,'hotel/index.html',context={'is_staff':1})
    try:
        user=AuthUser.objects.get(username=username)
        order=Order.objects.get(ordernum=order_num,hotelid=user.hotel_id)
        hotelinfo=HotelInfo.objects.get(id=order.hotelid)
        homeinfo=HomeInfo.objects.get(id=order.homeid)
        context = {
            'order': order,
            'homeinfo':homeinfo,
        }
        return render(request,'hotel/order-detail.html',context=context)
    except Order.DoesNotExist:
        return render(request, 'hotel/order_list.html')

# 全部交易信息渲染
def sale_info(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    if user.is_staff==1:
        return render(request,'hotel/index.html',context={'is_staff':1})
    order_list=Order.objects.filter(hotelid=user.hotel_id)
    today=timezone.localdate()
    total_year_order_price=0
    total_year_order=0
    total_month_order_price=0
    total_month_order=0
    total_day_order_price=0
    total_day_order=0
    for order in order_list:
        order_time=order.ordertime
        if order_time.strftime("%Y-%m-%d")==str(today):
            total_day_order=int(total_day_order)+1
            total_day_order_price=float(total_day_order_price)+float(order.price)
        if order_time.strftime("%Y-%m")=="{}-{}".format((str(today).split("-")[0]),(str(today).split("-")[1])):
            total_month_order=int(total_month_order)+1
            total_month_order_price=float(total_month_order_price)+float(order.price)
        if order_time.strftime("%Y")==str(today).split("-")[0]:
            total_year_order=int(total_year_order)+1
            total_year_order_price=float(total_year_order_price)+float(order.price)

    last_time=get_last_time(today)
    order_price=[]
    order_num=[]
    for i in range(len(last_time)):
        orders=Order.objects.filter(ordertime__year=last_time[i].split('-')[0],ordertime__month=last_time[i].split('-')[1],ordertime__day=last_time[i].split('-')[2])
        price=0
        for order in orders:
            price=float(price)+float(order.price)
        order_price.append(price)
        order_num.append(len(orders))

    order_price_url=pint(last_time,'日期',order_price,'订单收益','收益','销售额',HotelInfo.objects.get(id=user.hotel_id).name)
    order_num_url=pint(last_time,'日期',order_num,'订单数','数目','订单数据',HotelInfo.objects.get(id=user.hotel_id).name)

    context={
        'total_day_order':total_day_order,
        'total_day_order_price':total_day_order_price,
        'total_month_order':total_month_order,
        'total_month_order_price':total_month_order_price,
        'total_year_order':total_year_order,
        'total_year_order_price':total_year_order_price,
        'order_price_url':order_price_url,
        'order_num_url':order_num_url,
    }

    return render(request,'hotel/sale-info.html',context=context)

# 员工工资信息记录
def staff_pay(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    if user.is_staff==1:
        return render(request,'hotel/index.html',context={'is_staff':1})
    performance=0
    staff_num=0
    staff_price=0
    order_num=0
    staff_info={}
    try:
        staff_pay=StaffPay.objects.filter(hotelid=user.hotel_id)
        for staff in staff_pay:
            user=AuthUser.objects.get(id=staff.userid)
            name=Userinfo.objects.get(id=user.user_id)
            staff_info[name]=staff
            performance=performance+staff.performance
            staff_price=staff_price+staff.pay
    except:
        pass
    orders=Order.objects.filter(hotelid=user.hotel_id)
    order_num=len(orders)
    staff_users=AuthUser.objects.filter(hotel_id=user.hotel_id,is_staff=1)
    staff_num=len(staff_users)

    context={
        'staff_num':staff_num,
        'performance':performance,
        'staff_price':staff_price,
        'order_num':order_num,
        'staffs':staff_info,
    }
    return render(request,'hotel/staff-pay.html',context=context)


# 房屋清洁信息渲染
def home_clean_info(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    if user.is_staff==0:
        return redirect(reverse('hotel:backstage_index'))
    homes=HomeNum.objects.filter(hotelid=user.hotel_id)
    return render(request,'hotel/home-clean-info.html',context={'homes':homes})


# 员工工资信息页面渲染
def staff_wage(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    if user.is_staff==0:
        return redirect(reverse('hotel:backstage_index'))
    staff_wages=StaffPay.objects.filter(userid=user.id,hotelid=user.hotel_id)
    for staff in staff_wages:
        staff.date_pay=staff.date_pay.strftime("%m")
        staff.pay=float(staff.base_salary)+float(staff.performance)
    context={
        "staff_wage":staff_wages
    }
    return render(request,'hotel/staff-wage.html',context=context)


# 验证码
def verification(request):
    global  out_string,fill_point, fill_line
    out_string=''
    string_small = 'qwertyuiopasdfghjklzxcvbnm'
    string_big = string_small.upper()
    num = '0123456789'
    string = string_big + string_small + num
    mode = 'RGB'
    size = (100, 46)
    color = (248, 248, 255)
    image = Image.new(mode=mode, size=size, color=color)
    draw = ImageDraw.Draw(image, mode=mode)
    imagefont = ImageFont.truetype('/static/Font/Sitka.ttc', 30)
    # fill=(255,0,0)
    # draw.text(xy=(0,0),text='ad',font=imagefont,fill=fill)
    # 绘制干扰线
    for i in range(0, 15):
        begin = (random.randint(0, size[0]), random.randint(0, size[1]))
        end = (random.randint(0, size[0]), random.randint(0, size[1]))
        fill_line = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.line([begin, end], fill=fill_line)

    # 绘制干扰点
    for i in range(0, size[0]):
        for j in range(0, 10):
            fill_point = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw.point((random.randint(0, size[0]), random.randint(0, size[1])), fill=fill_point)

    # 绘制随机字符
    for i in range(0, 6):
        num = random.randint(0, len(string) - 1)
        fill_font = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if fill_line == fill_font or fill_point == fill_font:
            fill_font = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.text(xy=(random.uniform(16 * i, 15 * (i + 1)), 10), text=string[num], font=imagefont, fill=fill_font)
        out_string = out_string + string[num]

    fp = BytesIO()
    image.save(fp, 'png')
    print(out_string)
    return HttpResponse(fp.getvalue(), content_type='image/png')

# 酒店后台登录验证
def merchants_login(request):
    if request.POST:
        username=request.POST['username']
        hotel_name=request.POST['hotel_name']
        password=request.POST['password']
        code=request.POST['code']
        if out_string.upper()!=code.upper():
            # 验证码错误
            return render(request, 'hotel/login.html', context={"msg": "验证码错误，请重新填写"})
        try:
            # 查找酒店信息
            hotel=HotelInfo.objects.get(name=hotel_name)
            try:
                # 查找用户信息
                user=AuthUser.objects.get(username=username,hotel_id=hotel.id)
                if not check_password(password,user.password):
                    # 密码错误
                    return render(request, 'hotel/login.html', context={"msg": "密码错误，请确认后填写"})
                else:
                    request.session['username']=user.username
                    user.last_login=timezone.now()
                    user.save()
                    if user.is_staff == 1:
                        return render(request, 'hotel/index.html', context={'is_staff': 1})
                    return redirect(reverse("hotel:backstage_index"))
            except AuthUser.DoesNotExist:
                return render(request, 'hotel/login.html', context={"msg": "未查询到该用户，请确认用户后重新填写"})
        except HotelInfo.DoesNotExist:
            return render(request, 'hotel/login.html', context={"msg": "未查询到该酒店信息，请确认后重新输入"})
    else:
        return render(request, 'error-403.html')

# 酒店注册认证
def becom_merchants(request):
    if request.POST:
        username=request.POST['username']
        name=request.POST['name']
        hotel_name=request.POST['hotel_name']
        email=request.POST['email']
        password=request.POST['password']
        make_sure_password=request.POST['make_sure_password']
        code=request.POST['code']
        if make_sure_password!=password:
            # 确认密码错误
            return render(request, 'hotel/registration.html', context={"msg": "两次输入的密码不一致，请确认后输入"})
        if code.upper()!=out_string.upper():
            # 验证码错误
            return render(request, 'hotel/registration.html', context={"msg": "验证码错误，请重新填写"})
        hotel=HotelInfo(
            name=hotel_name
        )
        hotel.save()
        user_info=Userinfo(
            name=name
        )
        user_info.save()
        user=AuthUser(
            username=username,
            last_login=timezone.now(),
            email=email,
            is_staff=0,
            is_active=1,
            is_superuser=0,
            date_joined=timezone.now(),
            hotel_id=hotel.id,
            user_id=user_info.id,
            password=make_password(password=password),
        )
        user.save()
        return redirect(reverse("hotel:index"))
    else:
        return render(request, 'error-403.html')

# 员工首页渲染
def staff_index(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    if user.is_staff==0:
        return redirect(reverse('hotel:backstage_index'))
    userinfo=Userinfo.objects.get(id=user.user_id)
    context={
        'is_staff':user.is_staff,
        'userinfo':userinfo,
        'user':user
    }
    return render(request,'hotel/staff-info.html',context=context)

# 修改员工信息提交
def update_staff_info(request):
    if request.session.get('username'):
        return redirect(reverse('main:login'))
    if request.POST:
        name=request.POST['name']
        phone=request.POST['phone']
        address=request.POST['address']
        email=request.POST['email']
        code=request.POST['code']
        if code.upper()!=out_string.upper():
            return render(request,'hotel/staff-info.html')
        else:
            username=request.session.get('username')
            user=AuthUser.objects.get(username=username)
            user.email=email
            user.save()
            userinfo=Userinfo.objects.get(id=user.user_id)
            userinfo.name=name
            userinfo.phone=phone
            userinfo.address=address
            userinfo.save()
            return  redirect(reverse('hotel:staff_index'))
    else:
        return render(request,'error-403.html')

# 修改酒店信息
def submit_hotel_info(request):
    if not request.session.get('username'):
        return redirect(reverse('hotel:index'))
    if request.POST:
        username=request.session.get('username')
        name=request.POST['name']
        email=request.POST['email']
        user_phone=request.POST['user_phone']
        hotel_name=request.POST['hotel_name']
        hotel_address=request.POST['hotel_address']
        hotel_phone=request.POST['hotel_phone']
        hotel_opentime=request.POST['hotel_opentime']
        detail=request.POST['detail']
        hotel_city=request.POST['hotel_city']
        try:
            user=AuthUser.objects.get(username=username)
            user.email=email
            user.save()
            user_datail=Userinfo.objects.get(id=user.user_id)
            hotel_datail=HotelInfo.objects.get(id=user.hotel_id)
            user_datail.name=name
            user_datail.phone=user_phone
            user_datail.save()
            hotel_datail.name=hotel_name
            hotel_datail.detail=detail
            hotel_datail.address=hotel_address
            hotel_datail.phone=hotel_phone
            hotel_datail.open_time=hotel_opentime
            hotel_datail.city=hotel_city
            hotel_datail.save()
            context = {
                'username': username,
                'name': name,
                'email': email,
                'phone': user_phone,
                'hotel_name': hotel_name,
                'address': hotel_address,
                'hotel_phone': hotel_phone,
                'hotel_opentime': hotel_opentime,
                'hotel_detail': detail,
                'hotel_city': hotel_city
            }
            return render(request, 'hotel/hotel-info.html', context=context)
        except AuthUser.DoesNotExist:
            # 未找到当前用户名的数据信息
            request.session.flush()
            return redirect(reverse('main:login'))
        except Userinfo.DoesNotExist:
            # 未找到该用户详细信息
            user_datail=Userinfo(
                name=name,
                phone=user_phone,
            )
            user_datail.save()
            user.user_id=user_datail.id
            user.save()
            hotel_datail = HotelInfo.objects.get(id=user.hotel_id)
            hotel_datail.name = hotel_name
            hotel_datail.detail = detail
            hotel_datail.address = hotel_address
            hotel_datail.phone = hotel_phone
            hotel_datail.open_time = hotel_opentime
            hotel_datail.city = hotel_city
            hotel_datail.save()
            context={
                'username':username,
                'name':name,
                'email':email,
                'phone':user_phone,
                'hotel_name':hotel_name,
                'address':hotel_address,
                'hotel_phone':hotel_phone,
                'hotel_opentime':hotel_opentime,
                'hotel_detail':detail,
                'hotel_city':hotel_city
            }
            return render(request,'hotel/hotel-info.html',context=context)
        except HotelInfo.DoesNotExist:
            # 未找到酒店详细信息
            hotel_datail=HotelInfo(
                name=hotel_name,
                detail=detail,
                address=hotel_address,
                phone=hotel_phone,
                open_time=hotel_opentime,
                city=hotel_city,
            )
            hotel_datail.save()
            user.hotel_id=hotel_datail.id
            user.save()
            user_datail.name=name
            user_datail.phone=user_phone
            user_datail.save()
            context = {
                'username': username,
                'name': name,
                'email': email,
                'phone': user_phone,
                'hotel_name': hotel_name,
                'address': hotel_address,
                'hotel_phone': hotel_phone,
                'hotel_opentime': hotel_opentime,
                'hotel_detail': detail,
                'hotel_city': hotel_city
            }
            return render(request, 'hotel/hotel-info.html', context=context)
    else:
        return render(request,'error-403.html')

# 更新房型信息
def update_hometype(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    if request.POST:
        home_name = request.POST['home_name']
        price=request.POST['price']
        datail=request.POST['datail']
        num=request.POST['num']
        clean_price=request.POST['clean_price']
        code=request.POST['code']
        username=request.session.get('username')
        if code.upper()!=out_string.upper():
            return render(request,'hotel/home-info.html')
        try:
            user = AuthUser.objects.get(username=username)
            home_info=HomeInfo.objects.get(hotelid=user.hotel_id,name=home_name)
            home_info.price=price
            home_info.datail=datail
            home_info.num=num
            home_info.clean_price=clean_price
            home_info.save()
            return redirect(reverse('hotel:backstage_index'))
        except AuthUser.DoesNotExist:
            request.session.flush()
            return redirect(reverse('main:login'))
        except HomeInfo.DoesNotExist:
            home_info=HomeInfo(
                hotelid=user.hotel_id,
                name=home_name,
                price=price,
                datail=datail,
                num=num,
                clean_price=clean_price,
            )
            home_info.save()
            return redirect(reverse('hotel:backstage_index'))
    else:
        return render(request,'error-403.html')

# 更新房间信息
def update_homenum(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    if request.POST:
        home_num=request.POST['home_num']
        home_type=request.POST['home_type']
        is_clean=request.POST['is_clean']
        clean_user=request.POST['clean_user']
        code=request.POST['code']
        username=request.POST['username']
        if code.upper()!=out_string.upper():
            return render(request,'hotel/home-info.html')
        else:
            user=AuthUser.objects.get(username=username)
            homeid=HomeInfo.objects.get(hotelid=user.hotel_id,name=home_type).id
            home=HomeNum.objects.get(hotelid=user.hotel_id,num=home_num)
            home.homeid=homeid
            home.is_clean=is_clean
            home.clean_user=Userinfo.objects.get(name=clean_user).id
            home.save()
            return redirect(reverse('hotel:backstage_index'))
    else:
        return render(request,'error-403.html')

# 添加房型
def addhometype(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    if request.POST:
        home_type=request.POST['home_type']
        price=request.POST['price']
        datail=request.POST['datail']
        num=request.POST['num']
        clean_price=request.POST['clean_price']
        code=request.POST['code']
        username=request.session.get('username')
        if code.upper()!=out_string.upper():
            return render(request,'hotel/home-info.html')
        user=AuthUser.objects.get(username=username)
        hotel=HotelInfo.objects.get(id=user.hotel_id)
        home=HomeInfo(
            hotelid=hotel.id,
            name=home_type,
            price=price,
            datail=datail,
            num=num,
            clean_price=clean_price,
        )
        home.save()
        return redirect(reverse('hotel:home_info'))
    else:
        return render(request,'error-403.html')

# 添加房间
def addhomenum(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    if request.POST:
        home_num=request.POST['home_num']
        home_type=request.POST['home_type']
        code=request.POST['code']
        username=request.session.get('username')
        if code.upper()!=out_string.upper():
            return render(request,'hotel/home-info.html')
        user=AuthUser.objects.get(username=username)
        hotel_info=HotelInfo.objects.get(id=user.hotel_id)
        home_info=HomeInfo.objects.get(name=home_type)
        home_info.num=home_info.num+1
        home_info.save()
        num=HomeNum(
            hotelid=hotel_info.id,
            homeid=home_info.id,
            num=home_num,
            is_clean=1,
            is_live=0,
        )
        num.save()
        return redirect(reverse('hotel:backstage_index'))
    else:
        return render(request,'error-403.html')

# 修改个人信息
def update_userinfo(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    if request.POST:
        username=request.session.get('username')
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        qq=request.POST['qq']
        user=AuthUser.objects.get(username=username)
        user.email=email
        user.save()
        userinfo=Userinfo.objects.get(id=user.user_id)
        userinfo.name=name
        userinfo.phone=phone
        userinfo.qq=qq
        userinfo.save()
        return redirect(reverse('hotel:user_info'))
    else:
        return render(request, 'error-403.html')

# 添加员工信息
def add_staff(request):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    if request.POST:
        username=request.POST['username']
        name=request.POST['name']
        phone=request.POST['phone']
        password=request.POST['password']
        email=request.POST['email']
        base_salary=request.POST['base_salary']
        code=request.POST['code']
        if code.upper()!=out_string.upper():
            return redirect(reverse('hotel:user_info'))
        hotelid=AuthUser.objects.get(username=request.session.get('username')).hotel_id
        userinfo=Userinfo(
            name=name,
            phone=phone
        )
        userinfo.save()
        user=AuthUser(
            username=username,
            is_staff=1,
            hotel_id=hotelid,
            password=make_password(password),
            date_joined=timezone.now(),
            is_superuser=0,
            is_active=1,
            last_login=timezone.now(),
            user_id=userinfo.id,
            email=email,
        )
        user.save()
        staff=StaffPay(
            userid=user.id,
            hotelid=hotelid,
            base_salary=base_salary,
            date_pay=timezone.now().strftime("%Y-%m-01 00:00:00")
        )
        staff.save()
        return redirect(reverse('hotel:backstage_index'))
    else:
        return render(request, 'error-403.html')

# 房间清扫
def clean_home(request,home_num):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    userinfo=Userinfo.objects.get(id=user.user_id)
    homenum_info=HomeNum.objects.get(hotelid=user.hotel_id,num=home_num)
    home_info=HomeInfo.objects.get(hotelid=user.hotel_id,id=homenum_info.homeid)
    homenum_info.is_clean=1
    homenum_info.clean_user=userinfo.name
    homenum_info.save()
    home_clean_data=HomeCleanDate(
        hotelid=user.hotel_id,
        homenum=home_num,
        userid=user.id,
        clean_price=home_info.clean_price,
        is_clean=1,
        clean_date=timezone.now()
    )
    home_clean_data.save()
    try:
        # date_pay = timezone.localdate()
        date_pay = timezone.now().strftime("%Y-%m-01 00:00:00")
        print(date_pay)
        staff_pay = StaffPay.objects.get(userid=user.id, hotelid=user.hotel_id,date_pay=date_pay)
        staff_pay.performance = float(staff_pay.performance) + float(home_info.clean_price)
        staff_pay.clean_num=int(staff_pay.clean_num)+1
        staff_pay.save()
        return redirect(reverse('hotel:home_clean_info'))
    except StaffPay.DoesNotExist:
        base_salary=StaffPay.objects.filter(userid=user.id,hotelid=user.hotel_id)
        staff_pay=StaffPay(
            hotelid=user.hotel_id,
            userid=user.id,
            base_salary=base_salary[0].base_salary,
            performance=float(home_info.clean_price),
            clean_num=1,
            date_pay=date_pay
        )
        staff_pay.save()
        return redirect(reverse('hotel:home_clean_info'))


