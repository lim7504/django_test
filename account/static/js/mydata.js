//
//$(document).ready(function (e) {
//
//    var search_date_filter = getParameterByName('search_date_filter');
//    if(search_date_filter != "")
//    {
//        $('#search_date_filter').val(search_date_filter)
//    }
//});



$("#save").on("click", function (e) {

    var user_email = $("#user-email").val();
    var user_nick_name = $("#user-nick-name").val();
    var upload_file = $("#imgInput")[0].files[0];

    if( user_nick_name == "" )
    {
        alert("닉네임을 입력해 주세요.");
        return;
    }

    var formData = new FormData();
    formData.append("user_email", user_email);
    formData.append("user_nick_name", user_nick_name);
    formData.append("upload_file", upload_file);

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        async: true,
        type: 'POST',
        url: '/mydata/',
        contentType: false,
        processData: false,
        data: formData,
        success: function(response){

            if(response.status != 200){
                alert(response.message);
                return;
            }
            location.href = "/mydata/";

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
