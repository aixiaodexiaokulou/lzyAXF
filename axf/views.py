from django.shortcuts import render

# Create your views here.
from axf.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods


def home(request):  # 首页

    # 轮播图数据
    wheels = Wheel.objects.all()
    # nav数据
    navs = Nav.objects.all()
    # 必购数据
    mustbuys = Mustbuy.objects.all()

    # 便利店shop 商品部分
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    # 商品主体
    mainshows = MainShow.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
        'mainshows': mainshows,

    }
    return render(request, 'home/home.html', context=data)


# 闪购超市
def market(request, categoryid, childid, sortid):
    # 分类信息
    foodtypes = Foodtypes.objects.all()

    # 通过cookie获取点击下标  >>>对应>>> 分类ID
    typeIndex = int(request.COOKIES.get('typeIndex', 0))  # 默认热销榜点击
    # 根据分类下标获取对应的分类ID
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames
    # 将每个子类拆分出来

    # 商品信息（超多,所以只获取一部分）
    # goodslist = Goods.objects.all()[0:11]
    # 根据分类ID获取对应数据
    if childid == 0:
        goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childid)
    else:
        goodsList = Goods.objects.filter(categoryid=categoryid)

    childtypelist = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        dir = {
            'childname': arr[0],
            'childid': arr[1]
        }
        childtypelist.append(dir)


    # 排序
    if sortid == '1':   # 销量
        goodsList = goodsList.order_by('productnum')
    elif sortid == '2': # 价格↑
        goodsList = goodsList.order_by('price')
    elif sortid == '3': # 价格↓
        goodsList = goodsList.order_by('-price')

    data = {
        'foodtypes': foodtypes,  # 分类信息
        'goodsList': goodsList,  # 商品信息
        'childtypelist': childtypelist,  # 子类
        'categoryid': categoryid,  # 分类ID
        'childid':childid,         # 子类ID
    }

    return render(request, 'market/market.html', context=data)


# 购物车
def cart(request):
    return render(request, 'cart/cart.html')


# 我的
def mine(request):
    return render(request, 'mine/mine.html')
