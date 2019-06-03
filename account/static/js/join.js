$("#join").on("click", function (e) {
    var upload_file = $("#ingredient_file")[0].files[0];

    var user_email = $("#user-email").val();
    var user_nick_name = $("#user-nick-name").val();
    var user_password = $("#user-password").val();
    var user_password_confirm = $("#user-password-confirm").val();

    if( user_email == "" )
    {
        alert("이메일을 입력해 주세요.");
        return;
    }

    if( user_nick_name == "" )
    {
        alert("닉네임을 입력해 주세요.");
        return;
    }

    if( user_password == "" || user_password_confirm == "")
    {
        alert("비밀번호를 입력해 주세요.");
        return;
    }

    if( user_password != user_password_confirm )
    {
        alert("새 비밀번호와 비밀번호 확인이 일치하지 않습니다.");
        return;
    }


    var formData = new FormData();
    formData.append("user_email", user_email);
    formData.append("user_nick_name", user_nick_name);
    formData.append("user_password", user_password);

//    formData.append("upload_file", upload_file, upload_file.names);
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        async: true,
        type: 'POST',
        url: '/join/',
        contentType: false,
        processData: false,
        data: formData,
        success: function(response){

            if(response.status == 400){
                alert("같은 Email이 존재 합니다");
                return;
            }

            setCookie('access_token', response.access_token, '3');

            $.ajax({
                headers: { "Authorization": "Bearer " + getCookie("access_token") },
                type: 'GET',
                url: '/main/',
                success: function(response){
                    location.href = "/main/";
                    <!--alert("리다이렉트 성공!!");-->

                },
                error: function(request, status, error){
                    alert("system error!!")
                    console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                },
            });


        },
        error: function(request, status, error){
            alert("system error!!")
            console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
        },
    });
});



$("#file_download").on("click", function (e) {
    $.ajax({
        type: 'GET',
        <!--url: '/filedownload/',-->
        <!---->
        url:'/filedownload/',
        cache:false,
        xhr:function(){
            // Seems like the only way to get access to the xhr object
            var xhr = new XMLHttpRequest();
            xhr.responseType= 'blob'
            return xhr;
        },
        success: function(response){
            var img = document.getElementById('img');
            var img_a = document.getElementById('img_a');
            var url = window.URL || window.webkitURL;
            img.src = url.createObjectURL(response);
            alert(url.createObjectURL(response));
            alert("파일 Download Success!!");
        },
        error: function(request, status, error){
            alert("system error!!")
            console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
        },
    });
});

