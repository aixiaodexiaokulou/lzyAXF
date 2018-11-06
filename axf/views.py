import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from axf.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User
from python1809lzyAXF import settings


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
    # 获取用户信息
    token = request.session.get('token')
    responseDate = {}
    if token:
        user = User.objects.get(token=token)
        responseDate['name'] = user.name
        responseDate['rank'] = user.rank
        responseDate['img'] = '/static/uploads/' + user.img
    else:
        responseDate['name'] = '未登录'
        responseDate['rank'] = '暂无等级'
        responseDate['img'] = '/static/uploads/axf.png'


    return render(request, 'mine/mine.html',context=responseDate)

# 注册
def registe(request):
    if request.method == 'GET':
        return render(request, 'mine/registe.html')
    elif request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = request.POST.get('password')
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.addr = request.POST.get('addr')
        # user.img = 'axf.png'
        # 头像
        imgName = user.account + '.png'
        imagePath = os.path.join(settings.MEDIA_ROOT, imgName)
        file = request.FILES.get('icon')
        with open(imagePath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName

        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))
        user.save()
        # 状态保持
        request.session['token'] = user.token
        # 重定向
        return redirect('axf:mine')


def checkaccount(request):
    account = request.GET.get('account')
    # print(account)
    responseDate = {
        'msg': '账号可用',
        # 1表示可用 -1位不可用
        'status': 1,
    }
    try:
        user = User.objects.get(account=account)
        responseDate['msg'] = '账号已被占用'
        responseDate['status'] = -1
        return JsonResponse(responseDate)
    except:
        return JsonResponse(responseDate)
