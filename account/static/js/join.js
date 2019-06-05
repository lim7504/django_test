

$("#table-certificate-insert").on("click", function (e) {
    var row_count = $('#table-certificate tr').length;
    $('#table-certificate').append(
                                    '<tr>' +
                                           '<td> ' + row_count + ' </td>' +
                                        '<td>'+
                                            '<select>'+
                                                '<option disabled selected >자격증을 선택하세요.</option>'+
                                                '<option value="0">정보처리 기사</option>'+
                                                '<option value="1">정보처리 산업기사</option>'+
                                                '<option value="2">DAP</option>'+
                                                '<option value="3">SQLP</option>'+
                                            '</select>'+
                                        '</td>' +
                                        '<td>' +
                                            '<input type="date" class="form-control">' +
                                        '</td>' +
                                         '<td>' +
                                            '<input type="text">' +
                                        '</td>' +
                                        '<td style="text-align:center;"><button type="button" style="height:27px;  font-size:10px;" class="table-certificate-delete">삭제</button></td>' +
                                    '</tr>'
                                 );
});


$(".table-certificate-delete").on("click", function (e) {
    alert('asdfasdf');
//    var row = this.parentNode.parentNode;
//    row.parentNode.removeChild(row);
//
//    $("#table-certificate tr").each(function(index) {
//        <!--index 0번이 빈값으로 나오고 있음 1번부터가 index-->
//        if (index != 0 ) {
//
//            $row = $(this);
//
//            $(this).find('td:first').text(index);
//        }
//    });
});









$("#join").on("click", function (e) {
    var upload_file = $("#ingredient_file")[0].files[0];

    var user_email = $("#user-email").val();
    var user_nick_name = $("#user-nick-name").val();
    var user_password = $("#user-password").val();
    var user_password_confirm = $("#user-password-confirm").val();

//    var cert_id_array = $("input[name='certificate_id']").map(function(){return $(this).val();}).get();
//    var cert_name_array = $("select[name='certificate_name'] option:selected").map(function(){return $(this).val();}).get();
//    var cert_date_array = $("input[name='acquisition_date']").map(function(){return $(this).val();}).get();
//    var cert_no_array = $("input[name='certificate_no']").map(function(){return $(this).val();}).get();
//    var cert_row_state_array = $("input[name='certificate_row_state']").map(function(){return $(this).val();}).get();
//    alert(cert_name_array);

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
//    formData.append("cert_name_array", cert_name_array);
//    formData.append("cert_date_array", cert_date_array);
//    formData.append("cert_no_array", cert_no_array);

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
            alert("가입은 성공!!");
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

