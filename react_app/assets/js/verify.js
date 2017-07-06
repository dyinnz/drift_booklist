(function($) {
  'use strict';

    $(function () {
        $("#login_button").click(function () {
            console.log("click state");
            var name = $("#account").val();
            var pwd = $("#password_l").val();

            $.post("/login", { account: name, password: pwd }, function (data) {

                var obj = JSON.parse(data);

                if (obj.ok === 'true') {
                    alert("登录成功");
                    $(function () {
                        window.location.href = "/recommend";
                    })

                } else {
                    alert("登录失败");
                }
            });
        });

    });
})(jQuery);
