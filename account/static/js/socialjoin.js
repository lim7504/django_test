//
//
//$("#table-certificate-insert").on("click", function (e) {
//    var row_count = $('#table-certificate tr').length;
//    $('#table-certificate').append(
//                                    '<tr>' +
//                                           '<td> ' + row_count + ' </td>' +
//                                        '<td>'+
//                                            '<select>'+
//                                                '<option disabled selected >자격증을 선택하세요.</option>'+
//                                                '<option value="0">정보처리 기사</option>'+
//                                                '<option value="1">정보처리 산업기사</option>'+
//                                                '<option value="2">DAP</option>'+
//                                                '<option value="3">SQLP</option>'+
//                                            '</select>'+
//                                        '</td>' +
//                                        '<td>' +
//                                            '<input type="date" class="form-control">' +
//                                        '</td>' +
//                                         '<td>' +
//                                            '<input type="text">' +
//                                        '</td>' +
//                                        '<td style="text-align:center;"><button type="button" style="height:27px;  font-size:10px;" class="table-certificate-delete">삭제</button></td>' +
//                                    '</tr>'
//                                 );
//});
//
//
//$(".table-certificate-delete").on("click", function (e) {
//    alert('asdfasdf');
////    var row = this.parentNode.parentNode;
////    row.parentNode.removeChild(row);
////
////    $("#table-certificate tr").each(function(index) {
////        <!--index 0번이 빈값으로 나오고 있음 1번부터가 index-->
////        if (index != 0 ) {
////
////            $row = $(this);
////
////            $(this).find('td:first').text(index);
////        }
////    });
//});
//








$("#join").on("click", function (e) {

    var user_email = $("#user-email").val();
    var user_nick_name = $("#user-nick-name").val();

    var upload_file = $("#imgInput")[0].files[0];

//    var cert_id_array = $("input[name='certificate_id']").map(funsction(){return $(this).val();}).get();
//    var cert_name_array = $("select[name='certificate_name'] option:selected").map(function(){return $(this).val();}).get();
//    var cert_date_array = $("input[name='acquisition_date']").map(function(){return $(this).val();}).get();
//    var cert_no_array = $("input[name='certificate_no']").map(function(){return $(this).val();}).get();
//    var cert_row_state_array = $("input[name='certificate_row_state']").map(function(){return $(this).val();}).get();
//    alert(cert_name_array);


    if( user_nick_name == "" )
    {
        alert("닉네임을 입력해 주세요.");
        return;
    }


    var formData = new FormData();
    formData.append("user_nick_name", user_nick_name);

//    formData.append("cert_name_array", cert_name_array);
//    formData.append("cert_date_array", cert_date_array);
//    formData.append("cert_no_array", cert_no_array);
    formData.append("upload_file", upload_file);
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        async: true,
        type: 'POST',
        url: '/socialjoin/',
        contentType: false,
        processData: false,
        data: formData,
        success: function(response){

            if(response.status != 200){
                alert(response.message);
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

$("#user-profile").on("click", function (e) {

//    e.preventDefault();
    $("#imgInput").click();
});

$("#imgInput").on("change", function (e) {
//    e.preventDefault();
    if (this.files && this.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#user-profile').attr('src', e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    }
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

