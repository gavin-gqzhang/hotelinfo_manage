from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    hotel_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HomeCleanDate(models.Model):
    hotelid = models.IntegerField(blank=True, null=True)
    homenum = models.IntegerField(blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)
    clean_price = models.CharField(max_length=255, blank=True, null=True)
    is_clean = models.IntegerField(blank=True, null=True)
    clean_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'home_clean_date'


class HomeInfo(models.Model):
    hotelid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    datail = models.TextField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    clean_price = models.CharField(max_length=255, blank=True, null=True)
    live_num = models.IntegerField(blank=True, null=True)
    live_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'home_info'


class HomeNum(models.Model):
    hotelid = models.IntegerField(blank=True, null=True)
    homeid = models.IntegerField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    is_clean = models.IntegerField(blank=True, null=True)
    clean_user = models.IntegerField(blank=True, null=True)
    is_live = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'home_num'


class HotelInfo(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    open_time = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    city = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel_info'


class Order(models.Model):
    userid = models.IntegerField(blank=True, null=True)
    hotelid = models.IntegerField(blank=True, null=True)
    homeid = models.IntegerField(blank=True, null=True)
    home_num = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    intime = models.CharField(max_length=255, blank=True, null=True)
    ordertime = models.DateTimeField(blank=True, null=True)
    ordernum = models.CharField(max_length=255, blank=True, null=True)
    idcard = models.CharField(max_length=255, blank=True, null=True)
    check_in = models.IntegerField(blank=True, null=True)
    outtime = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    live_num = models.IntegerField(blank=True, null=True)
    is_departure = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class ResetPwdLog(models.Model):
    userid = models.IntegerField(blank=True, null=True)
    resetid = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reset_pwd_log'


class StaffPay(models.Model):
    userid = models.IntegerField(blank=True, null=True)
    hotelid = models.IntegerField(blank=True, null=True)
    base_salary = models.CharField(max_length=255, blank=True, null=True)
    pay = models.CharField(max_length=255, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    performance = models.CharField(max_length=255, blank=True, null=True)
    clean_num = models.IntegerField(blank=True, null=True)
    date_pay = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'staff_pay'


class Userinfo(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    qq = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userinfo'

