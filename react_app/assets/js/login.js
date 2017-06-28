(function ($) {
    'use strict';

    $(function () {
        var $fullText = $('.admin-fullText');
        $('#admin-fullscreen').on('click', function () {
            $.AMUI.fullscreen.toggle();
        });

        $(document).on($.AMUI.fullscreen.raw.fullscreenchange, function () {
            $fullText.text($.AMUI.fullscreen.isFullscreen ? '退出全屏' : '开启全屏');
        });

        /*
        function rpanel_click() {
            $('#register_panel').attr('class', '');
            $('#login_panel').attr('class', 'am-active');

            $('#panel0').attr('class', 'am-active am-in');
            $('#panel1').attr('class', '');
        }

        function lpanel_click() {
            $('#register_panel').attr('class', '');
            $('#login_panel').attr('class', 'am-active');

            $('#panel1').attr('class', 'am-active am-in');
            $('#panel0').attr('class', '');
        }*/

        /*
        $(document).ready(function (){
            $('#register_button').click(function () {
                alert("helloooooooooooooooooooo");
                $('#panel0').html('<form action="login" method="POST" class="am-form" id="rp2">\
                    <fieldset>\
                    <div class="am-form-group">\
                    <label for="account">User Name</label>\
                <input type="text" id="account" name="account" minlength="3" placeholder="请输入用户名"\
                class="am-form-field" required/>\
                </div>\
                <div class="am-form-group">\
                    <label for="password_l">Password</label>\
                    <input type="password" id="password_l" name="password" minlength="5" placeholder="请输入密码"\
                class="am-form-field" required/>\
                </div>\
                    <br/>\
                    <button class="myapp-login-button am-btn am-btn-secondary" id="login_button"\
                type="submit">SIGN IN\
                </button>\
                </fieldset>\
                <legend>Forgot Password?</legend>\
                </form>');
                alert("hellllllllllllllllllllllllllllllll");
            });
            /*$('#register_panel').click(function () {
                rpanel_click();
            });
            $('#login_panel').click(function () {
                lpanel_click();
            });*/

        });
        */

        /*
         var getWindowHeight = $(window).height(),
         myappLoginBg    = $('.myapp-login-bg');
         myappLoginBg.css('min-height',getWindowHeight + 'px');
         */
    });
})(jQuery);
