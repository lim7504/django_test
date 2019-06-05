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
$("#upload").on("click", function (e) {
    var upload_file = $("#ingredient_file")[0].files[0];
    var formData = new FormData();
    formData.append("upload_file", upload_file, upload_file.names);
    formData.append("upload_file", true);
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        async: true,
        type: 'POST',
        url: '/main/',
        contentType: false,
        processData: false,
        data: formData,
        success: function(response){
            alert("파일 업로드 Success!!");
        },
        error: function(request, status, error){
            alert("system error!!")
            console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
        },
    });
});

