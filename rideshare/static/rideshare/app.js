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

function passenger_cancel_ride_request() {
    console.log("passenger_cancel_ride_request")
    var id = parseInt($("#ride_id").html());
    $.ajax({
        method: "post",
        url: "/api/passenger_cancel_ride_request/",
        data: {
            "id": id,
        },
        statusCode: {
            302: function(resp) {
                console.log("302");
                window.location = resp.responseJSON.location;
            },
        },
        success: function(resp, status) {
            console.log("success");
            console.log(resp);
            window.location.href = "/upcoming_rides/";
        },
        error: function(resp) {
            console.log("error");
            console.log(resp);
        },
    });
}

function passenger_undo_cancel_ride_request() {
    console.log("passenger_undo_cancel_ride_request")
    var id = parseInt($("#ride_id").html());
    $.ajax({
        method: "post",
        url: "/api/passenger_undo_cancel_ride_request/",
        data: {
            "id": id,
        },
        statusCode: {
            302: function(resp) {
                console.log("302");
                window.location = resp.responseJSON.location;
            },
        },
        success: function(resp, status) {
            console.log("success");
            console.log(resp);
            window.location.href = "/upcoming_rides/";
        },
        error: function(resp) {
            console.log("error");
            console.log(resp);
        },
    });
}

function driver_claim_pickup() {
    console.log("driver_claim_pickup")
    var id = parseInt($("#ride_id").html());
    $.ajax({
        method: "post",
        url: "/api/driver_claim_pickup/",
        data: {
            "id": id,
        },
        statusCode: {
            302: function(resp) {
                console.log("302");
                window.location = resp.responseJSON.location;
            },
        },
        success: function(resp, status) {
            console.log("success");
            console.log(resp);
            window.location.href = "/driver/upcoming_rides/";
        },
        error: function(resp) {
            console.log("error");
            console.log(resp);
        },
    });
}

function driver_cancel_pickup() {
    console.log("driver_cancel_pickup")
    var id = parseInt($("#ride_id").html());
    $.ajax({
        method: "post",
        url: "/api/driver_cancel_pickup/",
        data: {
            "id": id,
        },
        statusCode: {
            302: function(resp) {
                console.log("302");
                window.location = resp.responseJSON.location;
            },
        },
        success: function(resp, status) {
            console.log("success");
            console.log(resp);
            window.location.href = "/driver/available_rides/";
        },
        error: function(resp) {
            console.log("error");
            console.log(resp);
        },
    });
}

function epoch_to_time(seconds) {
    var date = new Date(0);
    date.setUTCSeconds(seconds);
    var hours = date.getHours().toString();
    var minutes = date.getMinutes().toString();
    if (hours.length == 1) {
        hours = "0" + hours;
    }
    if (minutes.length == 1) {
        minutes = "0" + minutes;
    }
    var currentTime = hours + ':' + minutes;
    return currentTime;
}

function epoch_to_date(seconds) {
    console.log(seconds);
    var date = new Date(0);
    date.setUTCSeconds(seconds);
    var parts = date.toLocaleDateString();
    var year = parts.split("/")[2];
    var month = parts.split("/")[1];
    var day = parts.split("/")[0];
    year = year.toString();
    month = month.toString();
    day = day.toString();
    if (month.length == 1) {
        month = "0" + month;
    }
    if (day.length == 1) {
        day = "0" + day;
    }
    var format = year + "-" + day + "-" + month;
    console.log(format);
    return format;
}

/*------------------------------------------------------------------------------
STRIPE
------------------------------------------------------------------------------*/
function checkout(plan_id) {
    var stripe = Stripe("pk_test_QqesTZpsPOaT7vzdYMJ0kP6C00MGYz6SSf")
    $.ajax({
        url: "/api/stripe_checkout_session_id",
        method: "post",
        data: {
            plan_id: plan_id,
        },
        success: function(resp) {
            console.log("200");
            var checkout_session_id = resp.checkout_session_id;
            stripe.redirectToCheckout({
                // Make the id field from the Checkout Session creation API response
                // available to this file, so you can provide it as parameter here
                // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
                sessionId: checkout_session_id,
            }).then(function (result) {
                console.log("OK")
                // If `redirectToCheckout` fails due to a browser or network
                // error, display the localized error message to your customer
                // using `result.error.message`.
            });
        },
        error: function(resp) {
            console.log("500");
            console.log(resp);
        },
    });
}

function cancel_subscription_by_subscription_id(subscription_id) {
    var stripe = Stripe("pk_test_QqesTZpsPOaT7vzdYMJ0kP6C00MGYz6SSf")
    $.ajax({
        url: "/api/strip_cancel_subscription_by_subscription_id",
        method: "post",
        data: {
            subscription_id: subscription_id,
        },
        success: function(resp) {
            console.log("200");
            alert("Your subscription has been canceled.");
            location.reload();
        },
        error: function(resp) {
            console.log("500");
            console.log(resp);
            alert("There was a problem canceling your subscription.");
        },
    });
}
