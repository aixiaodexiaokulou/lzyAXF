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
