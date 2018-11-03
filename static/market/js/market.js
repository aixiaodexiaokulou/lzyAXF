$(function () {
    $('.market').width(innerWidth)

    //侧边栏分类
    $('.type-item').click(function () {
        // $(this).addClass('active')
        // 记录位置 设置cookie
        $.cookie('typeIndex', $(this).index(), {expires:3, path:'/'})

    })

    // 获取typeIndex 利用cookie的index添加类
    typeIndex = $.cookie('typeIndex')
    if(typeIndex){
        $('.type-slider .type-item').eq(typeIndex).addClass('active')
    }else {
        // 没有点击默认第一个
        $('.type-slider .type-item:first').addClass('active')
    }



    // 分类按钮
    categoryBt = false  // 默认隐藏
    $('#categoryBt').click(function () {
        categoryBt = !categoryBt    // 取反

        categoryBt ? categoryViewShow() : categoryViewHide()
    })


    // 排序按钮
    sortBt = false  // 也是默认隐藏
    $('#sortBt').click(function () {
        sortBt = !sortBt
        sortBt ? sortViewShow() : sortViewHide()

    })

    // 点击朦胧玻璃层
    $('.bounce-view').click(function () {
        categoryBt = false
        sortBt = false
        categoryViewHide()
        sortViewHide()
    })

    function categoryViewShow() {
        sortBt = false
        sortViewHide()
        $('.bounce-view.category-view').show()
        $('#categoryBt i').removeClass('glyphicon glyphicon-menu-up').addClass('glyphicon glyphicon-menu-down')
    }
    function categoryViewHide() {
        $('.bounce-view.category-view').hide()
        $('#categoryBt i').removeClass('glyphicon glyphicon-menu-down').addClass('glyphicon glyphicon-menu-up')
    }

    function sortViewShow() {
        categoryBt = false
        categoryViewHide()
        $('.bounce-view.sort-view').show()
        $('#sortBt i').removeClass('glyphicon glyphicon-menu-up').addClass('glyphicon glyphicon-menu-down')
    }
    function sortViewHide() {
        $('.bounce-view.sort-view').hide()
        $('#sortBt i').removeClass('glyphicon glyphicon-menu-down').addClass('glyphicon glyphicon-menu-up')
    }
})