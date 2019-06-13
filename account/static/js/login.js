$("#login").click(function(e){
    e.preventDefault();
    var email = $("#email").val();
    var password = $("#password").val();

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type: 'POST',
        url: '/',
        data: {
            'email': email,
            'password': password,
        },
        success: function(response){

            if(response.status != 200){
                alert("이메일과 비밀번호가 맞지 않습니다.");
                return;
            }

            setCookie('access_token', response.access_token, '3');
            location.href = "/main/";


        },
        error: function(request, status, error){
            alert("system error!!")
            console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
        },
    });
});
$("#join").click(function(e){
    e.preventDefault();
    $.ajax({
        type: 'GET',
        url: '/join/',
        success: function(response){
            location.href = "/join/";
            <!--alert("리다이렉트 성공!!");-->
        },
        error: function(request, status, error){
            alert("system error!!")
            console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
        },
    });
});
















//            $.ajax({
//                headers: { "Authorization": "Bearer " + getCookie("access_token") },
//                type: 'GET',
//                url: '/main/',
//                success: function(response){
//                    location.href = "/main/";
//                    <!--alert("리다이렉트 성공!!");-->
//
//                    },
//                error: function(request, status, error){
//                    alert("system error!!")
//                    console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
//                },
//            });