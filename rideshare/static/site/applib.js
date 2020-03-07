var applib = {
    init: function () {
        console.log("init");
    },
    forms: {
        request_a_ride: request_a_ride,
        rider_login: rider_login,
        driver_login: driver_login,
        rider_signup: rider_signup,
        driver_signup: driver_signup,
    }
}

/*------------------------------------------------------------------------------
Forms
------------------------------------------------------------------------------*/

function get_radio_bool(form_id, name) {
    value = "";
    radios = $("[name='" + name + "']");
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            value = radios[i].value;
            break;
        }
    }
    return value;
}

function driver_signup() {
    form_id = "FORM_driver_signup";
    // username = $("#" + form_id + " #username").val();
    pronoun = $("#" + form_id + " #pronoun :selected").val();
    first_name = $("#" + form_id + " #first_name").val();
    last_name = $("#" + form_id + " #last_name").val();
    contact_email = $("#" + form_id + " #contact_email").val();
    contact_phone = $("#" + form_id + " #contact_phone").val();
    // password = $("#" + form_id + " #password").val();
    // repeat_password = $("#" + form_id + " #repeat_password").val();
    smartphone_type = $("#" + form_id + " #smartphone_type").val();
    vehicle_year = $("#" + form_id + " #vehicle_year").val();
    vehicle_make = $("#" + form_id + " #vehicle_make").val();
    vehicle_model = $("#" + form_id + " #vehicle_model").val();
    vehicle_doors = $("#" + form_id + " #vehicle_doors").val();
    yes_no_square = get_radio_bool(form_id, "yes_no_square");
    yes_no_insurance = get_radio_bool(form_id, "yes_no_insurance");
    yes_no_criminal_history = get_radio_bool(form_id, "yes_no_criminal_history");
    comments = "";
    comments = $("#" + form_id + " #comments").val();
    errors = {};
    /*
    if (username == "") {
        errors["username"] = "Username is required."
    }
    */
    if (pronoun == "Pronoun") {
        errors["pronoun"] = "Pronoun is required."
    }
    if (first_name == "") {
        errors["first_name"] = "First name is required."
    }
    if (last_name == "") {
        errors["last_name"] = "Last name is required."
    }
    if (contact_email == "") {
        errors["contact_email"] = "Contact email is required."
    }
    if (contact_phone == "") {
        errors["contact_phone"] = "Contact phone is required."
    }
    /*
    if (password == "") {
        errors["password"] = "Password is required."
    }
    if (repeat_password == "") {
        errors["repeat_password"] = "Repeated password is required."
    }
    */
    if (smartphone_type == "Smartphone Type") {
        errors["smartphone_type"] = "Smartphone type is required."
    }
    if (vehicle_year == "Vehicle Year") {
        errors["vehicle_year"] = "Vehicle year is required."
    }
    if (vehicle_make == "Vehicle Make") {
        errors["vehicle_make"] = "Vehicle make is required."
    }
    if (vehicle_model == "") {
        errors["vehicle_model"] = "Vehicle model is required."
    }
    if (vehicle_doors == "Number of Doors") {
        errors["vehicle_doors"] = "Number of vehicle doors is required."
    }
    if (yes_no_square == "") {
        errors["yes_no_square"] = "Question about Square is required."
    }
    if (yes_no_insurance == "") {
        errors["yes_no_insurance"] = "Question about insurance is required."
    }
    if (yes_no_criminal_history == "") {
        errors["yes_no_criminal_history"] = "Question about criminal history is required."
    }
    if (comments == "") {
        // errors["comments"] = "Comments are required."
    }
    if (Object.keys(errors).length > 0) {
        console.log(errors);
        form_error(errors, form_id);
    } else {
        data = {
            "command": "driver_signup",
            // "username": username,
            "pronoun": pronoun,
            "first_name": first_name,
            "last_name": last_name,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            // "password": password,
            // "repeat_password": repeat_password,
            "smartphone_type": smartphone_type,
            "vehicle_year": vehicle_year,
            "vehicle_make": vehicle_make,
            "vehicle_model": vehicle_model,
            "vehicle_doors": vehicle_doors,
            "yes_no_square": yes_no_square,
            "yes_no_insurance": yes_no_insurance,
            "yes_no_criminal_history": yes_no_criminal_history,
            "comments": comments,
        }
        submit_form(form_id, data);
    }
}

function rider_signup() {
    form_id = "FORM_rider_signup";
    username = $("#" + form_id + " #username").val();
    pronoun = $("#" + form_id + " #pronoun :selected").val();
    first_name = $("#" + form_id + " #first_name").val();
    last_name = $("#" + form_id + " #last_name").val();
    password = $("#" + form_id + " #password").val();
    repeat_password = $("#" + form_id + " #repeat_password").val();
    errors = {};
    if (username == "") {
        errors["username"] = "Username is required."
    }
    if (pronoun == "Pronoun") {
        errors["pronoun"] = "Pronoun is required."
    }
    if (first_name == "") {
        errors["first_name"] = "First name is required."
    }
    if (last_name == "") {
        errors["last_name"] = "Last name is required."
    }
    if (password == "") {
        errors["password"] = "Password is required."
    }
    if (repeat_password == "") {
        errors["repeat_password"] = "Repeated password is required."
    }
    if (Object.keys(errors).length > 0) {
        console.log(errors);
        form_error(errors, form_id);
    } else {
        data = {
            "command": "rider_signup",
            "username": username,
            "pronoun": pronoun,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "repeat_password": repeat_password,
        }
        submit_form(form_id, data);
    }
}

function rider_login() {
    form_id = "FORM_rider_login";
    username = $("#" + form_id + " #username").val();
    password = $("#" + form_id + " #password").val();
    errors = {};
    if (username == "") {
        errors["username"] = "Username is required."
    }
    if (password == "") {
        errors["password"] = "Password is required."
    }
    if (Object.keys(errors).length > 0) {
        console.log(errors);
        form_error(errors, form_id);
    } else {
        data = {
            "command": "rider_login",
            "username": username,
            "password": password,
        }
        submit_form(form_id, data);
    }
}

function driver_login() {
    form_id = "FORM_driver_login";
    username = $("#" + form_id + " #username").val();
    password = $("#" + form_id + " #password").val();
    errors = {};
    if (username == "") {
        errors["username"] = "Username is required."
    }
    if (password == "") {
        errors["password"] = "Password is required."
    }
    if (Object.keys(errors).length > 0) {
        console.log(errors);
        form_error(errors, form_id);
    } else {
        data = {
            "command": "driver_login",
            "username": username,
            "password": password,
        }
        submit_form(form_id, data);
    }
}

function request_a_ride() {
    form_id = "FORM_request_a_ride";
    name = $("#" + form_id + " #name").val();
    pickup_time = $("#" + form_id + " #pickup_time").val();
    pickup_date = $("#" + form_id + " #pickup_date").val();
    phone_number = $("#" + form_id + " #phone_number").val();
    pronoun = $("#" + form_id + " #pronoun ").val();
    start_location = $("#" + form_id + " #start_location").val();
    end_location = $("#" + form_id + " #end_location").val();
    passenger_count = $("#" + form_id + " #passenger_count").val();
    num_bags = $("#" + form_id + " #num_bags").val();
    special_req = $("#" + form_id + " #special_req").val();
    errors = {};
    if (name == "") {
        errors["name"] = "Name is required."
    }
    if (pickup_time == "") {
        errors["pickup_time"] = "Pickup time is required."
    }
    if (pickup_date == "") {
        errors["pickup_date"] = "Pickup date is required."
    }
    function validate(phone_number) {
        const regex = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
        console.log(regex.test(phone_number))
        errors = {};
    }

    // validate('1234567890')     // true
    // validate(1234567890)       // true
    // validate('(078)789-8908')  // true
    // validate('123-345-3456')   // true
    
    if (validate(phone_number) == false) {
        console.log("+" + phone_number + "is not a valid phone number")
        errors["phone_number"] = "Please enter a valid 10-12 digit numeric phone number."
    }
    if (pronoun == "") {
        errors["pronoun"] = "Pronoun is required."
    }
    if (start_location == "") {
        errors["start_location"] = "Starting point is required."
    }
    if (end_location == "") {
        errors["end_location"] = "Destination is required."
    }
    if (passenger_count == "") {
        errors["passenger_count"] = "There must be at least one passenger."
    }
    if (num_bags == "") {
        errors["num_bags"] = "Number of bags is required."
    }
    if (special_req == "") {
        special_req = "None"
    }
    if (Object.keys(errors).length > 0) {
        console.log(errors);
        form_error(errors, form_id);
    } else {
        data = {
            "command": "request_a_ride",
            "name": name,
            "pickup_time": pickup_time,
            "pickup_date": pickup_date,
            "phone_number": phone_number,
            "pronoun": pronoun,
            "start_location": start_location,
            "end_location": end_location,
            "passenger_count": passenger_count,
            "num_bags": num_bags,
            "special_req": special_req,
        }
        submit_form(form_id, data);
    }


    /*------------------------------------------------------------------------------
    Form Utils
    ------------------------------------------------------------------------------*/

    function submit_form(form_id, data) {
        // var test = '6LeoZbYUAAAAAJAN7NGGbFuT8qNKGPdKyqG6IgRR';
        grecaptcha.ready(function () {
            console.log("FORM_ID: " + form_id);
            grecaptcha.execute(
                '6LeoZbYUAAAAAP3yjdxMcf4uLfxFDiE_razm0koU',
                { action: form_id })
                .then(function (token) {
                    console.log("DATA: ");
                    console.log(data);
                    console.log("TOKEN RECIEVED: " + token);
                    data['_grecaptcha_token'] = token;
                    $.ajax({
                        "url": "/",
                        "data": data,
                        "type": "POST",
                        "statusCode": {
                            200: function (resp) {
                                console.log("200");
                                console.log(resp);
                                clear_form_messages(form_id);
                                form_success([resp], form_id);
                                $("#" + form_id + " button").attr("onclick", "").unbind("click");
                            },
                            302: function (resp) {
                                console.log("302");
                                console.log(resp.responseText);
                                window.location.href = resp.responseText;
                            },
                            500: function (err) {
                                console.log("500");
                                console.error(err);
                                form_error(["There was an unknown error."], form_id);
                            },
                            503: function (err) {
                                console.log("503");
                                console.error(err);
                                form_error([
                                    "This service is temporarily down at this time."
                                ], form_id);
                            },
                            400: function (err) {
                                console.log("400");
                                console.log(err.responseText);
                                form_error([err.responseText], form_id);
                            },
                            403: function (err) {
                                console.log("403");
                                console.error(err);
                                form_error([err.responseText], form_id);
                            },
                            404: function (err) {
                                console.log("404");
                                console.error(err);
                                form_error([
                                    "This service is temporarily down at this time."
                                ], form_id);
                            },
                        }
                    })
                });
        });
    }

    function clear_form_messages(form_id) {
        $("#" + form_id).find("*").removeClass("input_error");
        $("#" + form_id + " .form_error").addClass("hidden");
        $("#" + form_id + " .form_error").html("");
        $("#" + form_id + " .form_success").addClass("hidden");
        $("#" + form_id + " .form_success").html("");
    }

    function form_error(errors, form_id) {
        clear_form_messages(form_id);
        ids = Object.keys(errors);
        messages = Object.values(errors);
        $("#" + form_id + " .form_error").html(messages.join("<br>"));
        $("#" + form_id + " .form_error").removeClass("hidden");
        for (i = 0; i < ids.length; i++) {
            id = ids[i];
            $("#" + form_id + " #" + id).addClass("input_error");
        }
    }

    function form_success(message, form_id) {
        clear_form_messages(form_id);
        $("#" + form_id + " .form_success").html(message);
        $("#" + form_id + " .form_success").removeClass("hidden");
    }
}