function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function clearDriverRideRequestCookies() {
    deleteCookie("sidebar_pinned");
    deleteCookie("start_address");
    deleteCookie("end_address");
    deleteCookie("originPlaceId");
    deleteCookie("destinationPlaceId");
    deleteCookie("pickup_time");
    deleteCookie("pickup_date");
}

function passenger_confirm_ride_request() {
    console.log("passenger_confirm_ride_request")
    $.ajax({
        method: "post",
        url: "/api/passenger_confirm_ride_request/",
        statusCode: {
            302: function(resp) {
                console.log("302");
                window.location = resp.responseJSON.location;
            },
        },
        success: function(resp, status) {
            console.log("success");
            console.log(status);
            console.log(resp.msg);
            $("#ajax_confirm_ride_request").removeClass("btn-primary");
            $("#ajax_confirm_ride_request").addClass("btn-success");
            $("#ajax_confirm_ride_request").html(resp.msg);
        },
        error: function(resp) {
            console.log("error");
            console.log(resp);
        },
    });
}
