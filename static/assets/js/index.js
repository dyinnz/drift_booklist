/**
 * Created by lpq_user on 17-6-23.
 */
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
        $(document).ready(function () {
            $('#register_button').click(function () {
                $('#input_username').hide();
            });
        });*/

        /*
         var getWindowHeight = $(window).height(),
         myappLoginBg    = $('.myapp-login-bg');
         myappLoginBg.css('min-height',getWindowHeight + 'px');
         */
    });
})(jQuery);