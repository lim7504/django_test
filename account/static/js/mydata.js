
$(document).ready(function (e) {

    var search_date_filter = getParameterByName('search_date_filter');
    if(search_date_filter != "")
    {
        $('#search_date_filter').val(search_date_filter)
    }
});



