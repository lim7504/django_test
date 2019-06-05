function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function setCookie(cookie_name, value, days) {
      var exdate = new Date();
      exdate.setDate(exdate.getDate() + days);

      var cookie_value = escape(value) + ((days == null) ? '' : ';    expires=' + exdate.toUTCString());
      document.cookie = cookie_name + '=' + cookie_value;
}
