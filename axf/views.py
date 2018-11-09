import hashlib
import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from axf.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart
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
    if sortid == '1':  # 销量
        goodsList = goodsList.order_by('productnum')
    elif sortid == '2':  # 价格↑
        goodsList = goodsList.order_by('price')
    elif sortid == '3':  # 价格↓
        goodsList = goodsList.order_by('-price')

    token =  request.session.get('token')
    carts = []
    if token:   # 根据用户呢获取对应用户下的购物车数据
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user)

    data = {
        'foodtypes': foodtypes,  # 分类信息
        'goodsList': goodsList,  # 商品信息
        'childtypelist': childtypelist,  # 子类
        'categoryid': categoryid,  # 分类ID
        'childid': childid,  # 子类ID
        'carts': carts,
    }

    return render(request, 'market/market.html', context=data)


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
        responseDate['isLogin'] = 1
    else:
        responseDate['name'] = '未登录'
        responseDate['rank'] = '暂无等级'
        responseDate['img'] = '/static/uploads/lzy1.png'

    return render(request, 'mine/mine.html', context=responseDate)


# 注册
def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()


def registe(request):
    if request.method == 'GET':
        return render(request, 'mine/registe.html')
    elif request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = genarate_password(request.POST.get('password'))
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


# 验证账号
def checkaccount(request):
    account = request.GET.get('account')

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


# 退出
def logout(request):
    request.session.flush()
    return redirect('axf:mine')


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            if user.password == genarate_password(password):  # 登录成功

                # 更新token
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')
            else:  # 登录失败
                return render(request, 'mine/login.html', context={'passwdErr': '密码错误!'})
        except:
            return render(request, 'mine/login.html', context={'acountErr': '账号不存在!'})


# 添加购物车操作
def addcart(request):

    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg':'添加购物车成功',
        'status':1,
    }
    if token:
        user = User.objects.get(token=token)
        goods = Goods.objects.get(pk=goodsid)

        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():  # 商品已存在购物车 只修改商品个数
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
            responseData['number'] = cart.number
        else:               # 不存在购物车 就要新加一条数据
            cart =Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

            responseData['number'] = cart.number

        return JsonResponse(responseData)
    else:
        # 发起AJAX请求不能重定向/跳转
        # return redirect('axf:login')
        responseData['msg'] = '未登录，请登录后操作'
        responseData['status'] = -1
        return JsonResponse(responseData)

# 减掉商品
def subcart(request):
    token = request.session.get('token')
    goodsid = request.GET.get('goodsid')


    user = User.objects.get(token=token)
    goods = Goods.objects.get(pk=goodsid)

    # 删减
    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number-1
    cart.save()

    responseData = {
        'msg':'购物车删减物品成功',
        'status':1,
        'number':cart.number,
    }


    return JsonResponse(responseData)

# 购物车
def cart(request):
    token = request.session.get('token')
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)


        return render(request, 'cart/cart.html',context={'carts':carts})
    else:
        return redirect('axf:login')
# 改变购物车选中状态
def changecartstatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    responseData = {
        'msg': '选中状态改变',
        'status': 1,
        'isselect': cart.isselect
    }

    return JsonResponse(responseData)

# 全选/取消全选
def changecartselect(request):
    isselect = request.GET.get('isselect')
    if isselect == 'true':
        isselect = True
    else:
        isselect = False

    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        cart.isselect = isselect
        cart.save()

    return JsonResponse({'msg':'反选操作成功', 'status':1})
