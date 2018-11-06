$(function () {
    $('.register').width(innerWidth)

    // 账号验证(blur: 失去焦点)
    $('#account input').blur(function () {
        // 正则表达式
        var reg = /^\w+$/
        if (reg.test($(this).val())) {  // 符合


            // 发起ajax请求验证账号是否可用
            $.get('/checkaccount/', {'account': $(this).val()}, function (response) {
                console.log(response)
                if (response.status == 1) {  //账号可用
                    $('#account i').html('')
                    $('#account').removeClass('has-error')
                    $('#account span').removeClass('glyphicon-remove')


                    $('#account').addClass('has-success')
                    $('#account span').addClass('glyphicon-ok')
                } else {              // 账号不可用
                    $('#account i').html(response.msg)
                    $('#account').removeClass('has-success')
                    $('#account span').removeClass('glyphicon-ok')

                    $('#account').addClass('has-error')
                    $('#account span').addClass('glyphicon-remove')
                }

            })

        } else {  // 不符合
            $('#account i').html('账号由数字字母下划线注册')
            $('#account').removeClass('has-success')
            $('#account span').removeClass('glyphicon-ok')

            $('#account').addClass('has-error')
            $('#account span').addClass('glyphicon-remove')
        }
    })

    // 密码验证
    $('#password input').blur(function () {
        // 正则表达式
        var reg = /^\d{6,12}$/
        if (reg.test($(this).val())) {  // 符合
            $('#password i').html('')
            $('#password').removeClass('has-error')
            $('#password span').removeClass('glyphicon-remove')


            $('#password').addClass('has-success')
            $('#password span').addClass('glyphicon-ok')
        } else {  // 不符合
            $('#password i').html('6-12位数字')
            $('#password').removeClass('has-success')
            $('#password span').removeClass('glyphicon-ok')

            $('#password').addClass('has-error')
            $('#password span').addClass('glyphicon-remove')
        }
    })

    // 确认密码
    $('#passwd input').blur(function () {
        // 正则表达式
        var reg = /^\d{6,12}$/
        if ($(this).val() == $('#password input').val()) {  // 符合
            $('#passwd i').html('')
            $('#passwd').removeClass('has-error')
            $('#passwd span').removeClass('glyphicon-remove')


            $('#passwd').addClass('has-success')
            $('#passwd span').addClass('glyphicon-ok')
        } else {  // 不符合
            $('#passwd i').html('两次密码输入不一致')
            $('#passwd').removeClass('has-success')
            $('#passwd span').removeClass('glyphicon-ok')

            $('#passwd').addClass('has-error')
            $('#passwd span').addClass('glyphicon-remove')
        }
    })

    // 昵称
    $('#name input').blur(function () {
        // 正则表达式
        if ($(this).val() != '') {  // 符合
            $('#name i').html('')
            $('#name').removeClass('has-error')
            $('#name span').removeClass('glyphicon-remove')


            $('#name').addClass('has-success')
            $('#name span').addClass('glyphicon-ok')
        } else {  // 不符合
            $('#name i').html('昵称不能为空')
            $('#name').removeClass('has-success')
            $('#name span').removeClass('glyphicon-ok')

            $('#name').addClass('has-error')
            $('#name span').addClass('glyphicon-remove')
        }
    })

    // 手机验证
    $('#phone input').blur(function () {
        // 正则表达式
        var reg = /^1[34578]\d{9}$/
        if (reg.test($(this).val())) {  // 符合
            $('#phone i').html('')
            $('#phone').removeClass('has-error')
            $('#phone span').removeClass('glyphicon-remove')


            $('#phone').addClass('has-success')
            $('#phone span').addClass('glyphicon-ok')

        } else {  // 不符合
            $('#phone i').html('请输入正确的手机号')
            $('#phone').removeClass('has-success')
            $('#phone span').removeClass('glyphicon-ok')

            $('#phone').addClass('has-error')
            $('#phone span').addClass('glyphicon-remove')
        }
    })

})