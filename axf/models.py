from django.db import models

# Create your models here.
# 基础类
class Base(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    # 商品id
    trackid = models.CharField(max_length=10)
    # 不创建基础表
    class Meta:
        abstract = True

# 轮播图
class Wheel(Base):
    class Meta:
        db_table = 'axf_wheel'

# nav导航
class Nav(Base):
    class Meta:
        db_table = 'axf_nav'

# 每日必购
class Mustbuy(Base):
    class Meta:
        db_table = 'axf_mustbuy'

# 闪购shop 商品部分
class Shop(Base):
    class Meta:
        db_table = 'axf_shop'

# 商品主体
class MainShow(models.Model):
    trackid = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=8)
    brandname = models.CharField(max_length=50)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=8)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField()
    marketprice1 = models.FloatField()

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=8)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField()
    marketprice2 = models.FloatField()

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=8)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField()
    marketprice3 = models.FloatField()

    class Meta:
        db_table = 'axf_mainshow'

# 闪购超市部分
# 商品分类（侧边栏）
class Foodtypes(models.Model):  # 顶部
    typeid = models.CharField(max_length=8)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=256)

    # 显示先后顺序
    typesort = models.IntegerField()

    class Meta:
        db_table = 'axf_foodtypes'
# axf_goods(,,,,,,,,,,,,,,)
# 商品信息
class Goods(models.Model):
    productid = models.CharField(max_length=10)
    productimg = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)

    productlongname = models.CharField(max_length=100)

    # 精选
    isxf = models.BooleanField(default=False)
    # 买一送一
    pmdesc = models.BooleanField(default=False)
    # 规格
    specifics = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=7, decimal_places=2)
    marketprice = models.DecimalField(max_digits=7, decimal_places=2)

    # 分类ID
    categoryid = models.IntegerField()

    # 子类ID
    childcid = models.IntegerField()

    # 分类名称
    childcidname = models.CharField(max_length=100)

    # 详情ID
    dealerid = models.CharField(max_length=10)

    # 库存
    storenums = models.IntegerField()

    # 销量
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'

class User(models.Model):
    account = models.CharField(max_length=90, unique=True)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    addr = models.CharField(max_length=256)
    # 头像
    img = models.CharField(max_length=100)
    # 等级
    rank = models.IntegerField(default=1)
    # token
    token = models.CharField(max_length=256)

    class Meta:
        db_table = 'axf_user'
