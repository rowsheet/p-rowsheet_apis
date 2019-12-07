var sidebar = {
    toggle: () => {
        if ($("body").hasClass("sidebar_on")) {
            $("body").removeClass("sidebar_on");
        } else {
            $("body").addClass("sidebar_on");
        }
    }
}
var tabslide = {
    set: (selector, index) => {
        console.log(selector);
        $(selector + " .tabslide").css("margin-left", "-" + index + "00%");
        $(selector + " .tabnav").children().find("a").removeClass("active");
        $(selector + " .tabnav").children().find("a").eq(index).addClass("active");
    }
}
var rowsheet = {
    tabslide: tabslide,
    sidebar: sidebar,
}
