$(document).ready(function() {
    $('.ui.selection.dropdown').dropdown();
    $('.ui.button.btn_clear').on('click', function() {
        $('.ui.selection.dropdown').dropdown('clear'); // 清空
    });
    // 取出所有ans，写入input，注意如果用户输入有空格会导致ans出现'+'号，需要去除
    url = window.location.href;
    var arr = url.split('&ans='); // 以&ans=分割
    if (arr.length == 11) { // arr[1~10]为上一次input的值，将其恢复
        var inputs = document.getElementsByName('ans');
        for (var i = 0; i < inputs.length; i++) {
            // 先将arr[i+1]中的加号去掉
            inputs[i].value = arr[i + 1].replace(/[+]/g, '')
        }
    }
    $('.ui.button.confirm').on('click', function() {
        // 清空 Your Answer
        var inputs = document.getElementsByName('ans');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].value = '';
        }
    });
    // 登录窗口
    $('.ui.button.login').on('click', function() {
        $('.ui.mini.modal.login').modal('show');
    });
    // 登录菜单
    $('.ui.inline.dropdown').dropdown();
});