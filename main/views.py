from io import BytesIO
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
from PIL import Image, ImageDraw, ImageFont
from django.urls import reverse
from main.function import *
from main.models import *


# Create main views here.

# 首页页面信息渲染与回显
def index(request):
    username=request.session.get("username")
    return render(request, 'index/index.html', context={"username":username})


# 用户登录页面渲染
def login(request):
    return render(request, 'index/login.html')


# 用户注册页面渲染
def regist(request):
    return render(request, 'index/registration.html')


# 用户重置密码页面渲染
def reset_password(request):
    return render(request, 'index/reset-password.html')


# 订单页面渲染
def order_page(request,hotel_id,home_id):
    if not request.session.get('username'):
        return redirect(reverse('main:login'))
    else:
        username=request.session.get('username')
        user=AuthUser.objects.get(username=username)
        if user.hotel_id!=-1:
            request.session.flush()
            return redirect(reverse('main:login'))
        userinfo=Userinfo.objects.get(id=user.user_id)
        hotelinfo=HotelInfo.objects.get(id=hotel_id)
        homeinfo=HomeInfo.objects.get(id=home_id)
        context={
            'username':username,
            'userinfo':userinfo,
            'hotel_info':hotelinfo,
            'home_info':homeinfo,
            'user_time':get_time(),
            'get_minute':get_minute()
        }
        return render(request,'order/order.html',context=context)


# 登出
def sign_out(request):
    request.session.flush()
    return redirect(reverse('main:login'))


# 登录验证
def login_ver(request):
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        vr_code=request.POST['code']
        # 验证码是否正确
        if vr_code.upper()!=out_string.upper():
            return render(request,'index/login.html',context={"msg":"验证码错误"})
        try:
            user=AuthUser.objects.get(username=username)
            # 验证密码是否正确
            if not check_password(password,user.password):
                return render(request,'index/login.html',context={"msg":"密码错误，若忘记密码，可进行密码修改"})
            else:
                request.session['username']=username
                user.last_login=timezone.now()
                user.save()
                return redirect(reverse('main:index'))
        except AuthUser.DoesNotExist:
            return render(request, 'index/login.html', context={"msg": "未检测到该用户，请确认后填写，若无账户，请申请一个新的账户"})
        except:
            return render(request, 'error-500.html', context={"msg": "登录"})
    else:
        return render(request,'error-403.html')


# 注册验证
def regist_ver(request):
    if request.POST:
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        pwd = request.POST['password']
        make_sure_pwd = request.POST['make_sure_password']
        ver_code = request.POST['code']
        # 确认密码是否正确
        if pwd != make_sure_pwd:
            return render(request, 'index/registration.html', context={"msg": "两次输入的密码不一致"})
        # 确认验证码是否正确
        if ver_code.upper() != out_string.upper():
            return render(request, 'index/registration.html', context={"msg": "验证码错误，请重新填写"})

        # 确认密码和验证码验证成功
        try:
            userinfo = Userinfo(name=name)
            userinfo.save()
            user = AuthUser(user_id=userinfo.id, password=make_password(pwd), last_login=timezone.now(),
                            username=username, email=email, is_active=1, date_joined=timezone.now(), is_staff=0,
                            is_superuser=0,hotel_id=-1)
            user.save()
            return  redirect(reverse('main:login'))
        except:
            return render(request, 'error-500.html', context={"msg": "注册"})
    else:
        return  render(request,'error-403.html')


# 密码重置验证
def reset_ver(request):
    if request.POST:
        username=request.POST['username']
        email=request.POST['email']
        ver_code=request.POST['code']
        # 确认验证码是否正确
        if ver_code.upper() != out_string.upper():
            return render(request, 'index/registration.html', context={"msg": "验证码错误，请重新填写"})
        try:
            user=AuthUser.objects.get(username=username,email=email)
            # 发送邮件
            reset_code=''.join(i for i in random.sample("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890",random.randint(10,40)))
            send_mail("修改密码",message={"reset_code":reset_code})
            try:
                # 有重置记录，进行覆盖
                reset_pwd_log=ResetPwdLog.objects.get(userid=user.id)
                reset_pwd_log.resetid=reset_code
                reset_pwd_log.date=timezone.now()
                reset_pwd_log.save()
            except ResetPwdLog.DoesNotExist:
                #无重置记录，添加新的重置记录
                reset_pwd_log=ResetPwdLog(userid=user.id,resetid=reset_code,date=timezone.now())
                reset_pwd_log.save()
            return redirect(reverse('main:index'))
        except AuthUser.DoesNotExist:
            return render(request,'index/reset-password.html',context={"msg":"未检测到该用户，请检查自己输入的用户名或邮箱"})
        except:
            return render(request, 'error-500.html', context={"msg": "申请重置密码"})
    else:
        return render(request, 'error-403.html')


# 重置密码确认邮箱
def make_sure_email(request,reset_code):
    try:
        userid=ResetPwdLog.objects.get(resetid=reset_code).userid
        user=AuthUser.objects.get(id=userid)
        message={
            'username':user.username,
            'email':user.email,
        }
        return render(request,'index/reset.html',context=message)
    except ResetPwdLog.DoesNotExist:
        return HttpResponse("邮箱确认错误，请确认链接是否正确，从邮箱中点击链接！")


# 通过个人申请修改密码
def my_home_reset_password(request):
    if request.session.get('username')==None:
        return redirect(reverse('main:login'))
    username=request.session.get('username')
    user=AuthUser.objects.get(username=username)
    email=user.email
    context={
        'username':username,
        'email':email
    }
    return  render(request,'index/reset.html',context=context)

# 重置密码
def change_password(request):
    if request.POST:
        username=request.POST['username']
        email=request.POST['email']
        pwd=request.POST['password']
        make_sure_password=request.POST['make_sure_password']
        ver_code=request.POST['code']
        # 确认验证码是否正确
        if ver_code.upper() != out_string.upper():
            return render(request, 'index/reset.html', context={"msg": "验证码错误，请重新填写"})
        # 确认两个密码是否一致
        if pwd != make_sure_password:
            return render(request, 'index/reset.html', context={"msg": "两次输入的密码不一致"})
        try:
            user=AuthUser.objects.get(username=username,email=email)
            user.password=make_password(pwd)
            user.save()
            request.session.flush()
            return redirect(reverse('main:login'))
        except AuthUser.DoesNotExist:
            return render(request, 'index/reset.html', context={"msg": "请确认输入的用户名与邮箱"})
    else:
        return render(request, 'error-403.html')


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


# 个人后台首页
def my_home(request):
    if request.session.get('username') == None:
        # 未登录
        return redirect(reverse('main:login'))
    else:
        username=request.session.get('username')
        try:
            # 检查当前登录的用户名数据库中是否存储，若用户名异常则退出
            user = AuthUser.objects.get(username=username)
            if user.hotel_id!=-1 and user.is_staff==1:
                return redirect(reverse('hotel:staff_index'))
            if user.hotel_id!=-1 and user.is_staff==0:
                return redirect(reverse('hotel:backstage_index'))
            try:
                # 若在用户详细信息中没有存储该用户的信息，则进行新创建一个用户
                userinfo=Userinfo.objects.get(id=user.user_id)
            except Userinfo.DoesNotExist:
                userinfo=Userinfo(name='xczsdqrsdf123asd5')
                userinfo.save()
                user.user_id=userinfo.id
                user.save()
            email=user.email
            name=userinfo.name
            phone=userinfo.phone
            add=userinfo.address
            context = {
                'username':username,
                'email':email,
                'name':name,
                'phone':phone,
                'address':add,
                'qq':userinfo.qq,
            }
            return render(request, 'my_backstage/about_me.html', context=context)
        except AuthUser.DoesNotExist:
            # 若未查询到当前用户
            request.session.flush()
            return redirect(reverse('main:login'))

# 酒店列表罗列
def hotel_list(request):
    username = request.session.get('username')
    try:
        hotels=HotelInfo.objects.all()
        content={
            'username':username,
            'hotel_list':hotels,
        }
        return render(request,'index/hotels.html',context=content)
    except:
        content = {
            'username': username,
            'hotel_list': None,
        }
        return render(request,'index/hotels.html',context=content)


# 通过距离搜索酒店信息
def search_by_distance(request):
    if request.POST:
        distination=request.POST['distination']
        distance=request.POST['distance']
        ctx = {}
        hotel_list = []
        hotel_datail=HotelInfo.objects.all()
        ctx['lng1'] = address(distination)['lng']
        ctx['lat1'] = address(distination)['lat']
        for hotel in hotel_datail:
            ctx['lng2'] = address(hotel.address)['lng']
            ctx['lat2'] = address(hotel.address)['lat']
            d = get_distance_hav(ctx['lat1'], ctx['lng1'], ctx['lat2'], ctx['lng2'])
            if float(d) <= float(distance):
                hotel_list.append(hotel)
        context={
            "username":request.session.get('username'),
            "hotel_list":hotel_list
        }
        return render(request,'index/hotels.html',context=context)
    else:
        return render(request,'error-403.html')


# 通过名称搜索酒店信息
def search_by_name(request):
    if request.POST:
        hotel_name=request.POST['name']
        city=request.POST['city']
        try:
            # 模糊查询酒店信息，根据名称和城市
            hotel_list=HotelInfo.objects.filter(name__contains=hotel_name,city__contains=city)
            return render(request,'index/hotels.html',context={"username":request.session.get('username'),"hotel_list":hotel_list})
        except:
            return render(request,'index/hotels.html',context={"username":request.session.get('username'),"hotel_list":None})
    else:
        return render(request,'error-403.html')


# 酒店详细信息
def hotel_datail(request,hotel_name):
    try:
        hotelinfo=HotelInfo.objects.get(name=hotel_name)

        # 自主退宿
        try:
            orders = Order.objects.get(hotelid=hotelinfo.id)
            time = timezone.localdate()
            year = time.strftime('%Y')
            mouth = time.strftime('%m')
            day = time.strftime('%d')
            for order in orders:
                # 未离店的办理离店
                if order.is_departure == 0:
                    out_time = order.outtime
                    if int(out_time.split("-")[0]) < int(year) or int(
                            out_time.split("-")[1] < int(mouth) or int(out_time.split("-")[2] <= int(day))):
                        order.is_departure = 1
                        order.save()
                        home = HomeInfo.objects.get(id=order.homeid, hotelid=order.hotelid)
                        home.num = int(home.num) + 1
                        home.save()

        except Order.DoesNotExist:
            pass

        homeinfo=HomeInfo.objects.filter(hotelid=hotelinfo.id)

        context={
            'username':request.session.get('username'),
            'homeinfo':homeinfo,
            'hotelinfo':hotelinfo
        }
        return render(request,'index/homes.html',context=context)
    except HotelInfo.DoesNotExist:
        return redirect(reverse('main:index'))

# 修改个人信息
def change_info(request):
    if request.session.get('username')==None:
        return  redirect(reverse('main:login'))
    if request.POST:
        username=request.POST['username']
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        qq=request.POST['QQ']
        address=request.POST['address']
        try:
            # 若获取不到当前登录用户的用户信息，退出重新登录
            user=AuthUser.objects.get(username=username)
            user.email=email
            user.save()
            userinfo=Userinfo.objects.get(id=user.user_id)
            userinfo.name=name,
            userinfo.phone=phone
            userinfo.qq=qq
            userinfo.address=address
            userinfo.save()
            return redirect(reverse('main:home'))
        except:
            request.session.flush()
            return redirect(reverse('main:login'))
    else:
        return render(request,'error-403.html')


# 个人订单列表显示
def order_list(request):
    if request.session.get('username') == None:
        # 未登录
        return redirect(reverse('main:login'))
    else:
        username=request.session.get('username')
        try:
            user = AuthUser.objects.get(username=username)
            order_lists=Order.objects.filter(userid=user.id)
            context={
                'order_list':order_lists,
                'hotel_list':HotelInfo.objects.all(),
                'home_list':HomeInfo.objects.all()
            }
            return render(request,'my_backstage/order.html',context=context)
        except AuthUser.DoesNotExist:
            request.session.flush()
            return  redirect(reverse('main:login'))


# 确认入住（点击订单列表对应的按钮确认入住，跳转至信息详情页面完善个人登记信息
def to_stay_in(request,order_num):
    if request.session.get('username')==None:
        return  redirect(reverse('main:login'))
    try:
        order=Order.objects.get(ordernum=order_num)
        hotelinfo=HotelInfo.objects.get(id=order.hotelid)
        homeinfo=HomeInfo.objects.get(id=order.homeid)
        home_nums = HomeNum.objects.filter(hotelid=hotelinfo.id, homeid=homeinfo.id)

        context={
            'username':request.session.get('username'),
            'order':order,
            'hotelinfo':hotelinfo,
            'homeinfo':homeinfo,
            'homenums':home_nums,
        }
        return render(request,'order/stay_in.html',context=context)
    except Order.DoesNotExist:
        # 若没有该订单号
        return redirect(reverse('main:order_list'))


# 提交订单并创建订单
def submit_order(request):
    if request.session.get('username')==None:
        return redirect(reverse('main:login'))
    if request.POST:
        username=request.session.get('username')
        hotel_name=request.POST['hotel_name']
        home_name=request.POST['home_name']
        home_price=request.POST['home_price']
        get_day=request.POST['get_day']
        get_time=request.POST['get_time']
        data=request.POST['data']
        name=request.POST['name']
        phone=request.POST['phone']
        id_card=request.POST['id_card']
        live_num=request.POST['live_num']
        try:
            user=AuthUser.objects.get(username=username)
            hotelinfo = HotelInfo.objects.get(name=hotel_name)
            homeinfo = HomeInfo.objects.get(name=home_name, price=home_price)
            home_nums=HomeNum.objects.filter(hotelid=hotelinfo.id,homeid=homeinfo.id)

            order=Order(
                userid=user.id,
                hotelid=hotelinfo.id,
                homeid=homeinfo.id,
                name=name,
                phone=phone,
                intime="{0} {1}".format(get_day,get_time),
                days=data,
                idcard=id_card,
                price=float(home_price)*int(data),
                live_num=live_num,
                ordernum=''.join(i for i in random.sample("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890",random.randint(10,40))),
                ordertime=timezone.now(),
                outtime=get_out_time(get_day,data),
                check_in=0
            )
            order.save()
            homeinfo.num=int(homeinfo.num)-1
            homeinfo.save()
            return redirect(reverse('main:order_list'))
        except:
            return render(request, 'error-500.html', context={"msg": "订单提交"})
    else:
        return render(request, 'error-403.html')


# 订单确认并入住
def order_sure(request):
    if request.session.get('username')==None:
        return redirect(reverse('main:login'))
    if request.POST:
        order_num=request.POST['order_num']
        live_num=request.POST['live_num']
        name=request.POST['name']
        phone=request.POST['phone']
        id_card=request.POST['id_card']
        home_num=request.POST['home_num']
        try:
            order = Order.objects.get(ordernum=order_num)
            order.live_num=live_num
            order.name=name
            order.phone=phone
            order.idcard=id_card
            order.home_num=home_num
            order.check_in=1
            order.save()
            home_info=HomeNum.objects.get(hotelid=order.hotelid,homeid=order.homeid,num=home_num)
            home_info.is_live=1
            home_info.is_clean=0
            home_info.save()
            return redirect(reverse('main:order_datail',kwargs={'order_num':order_num}))
        except Order.DoesNotExist:
            return redirect(reverse('main:order_list'))
    else:
        return render(request, 'error-403.html')


# 订单详情
def order_datail(request,order_num):
    if request.session.get('username')==None:
        return redirect(reverse('main:login'))
    try:
        order=Order.objects.get(ordernum=order_num)
    except Order.DoesNotExist:
        return redirect(reverse('main:order_list'))
    hotelinfo = HotelInfo.objects.get(id=order.hotelid)
    homeinfo = HomeInfo.objects.get(id=order.homeid)
    if order.home_num == -1:
        home_nums = HomeNum.objects.filter(hotelid=hotelinfo.id, homeid=homeinfo.id)
        for i in range(len(home_nums)):
            home = home_nums[random.randint(0, len(home_nums))]
            if home.isclean == 1:
                order.home_num = home.num
                order.save()
                break
    context={
        'username':request.session.get('username'),
        'hotelinfo':hotelinfo,
        'homeinfo':homeinfo,
        'order':order
    }
    return render(request,'order/order_datail.html',context=context)
