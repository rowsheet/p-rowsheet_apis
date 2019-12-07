window.onload = function() {
    var anchors = {};
    var positions = [];
    document.querySelectorAll(".anchor").forEach(function(e) {
        positions.push(e.offsetTop);
        anchors[e.offsetTop] = e.id;
    });
    window.onscroll = function() {
        var scrollPosition =
        document.documentElement.scrollTop || document.body.scrollTop;

        var limit = scrollPosition + (screen.height / 4);
        var above = positions.filter(x => x < limit);
        var max = Math.max.apply(Math, above);
        var target = anchors[max];

        var link_selector = 'a[href="#' + target + '"].scrollspy';
        var title_selector = '#' + target + "_title";
        var show_key = "#show_" + $(link_selector).attr("data-show-key");
        console.log("show_key: " + show_key);
        var show_key_expanded = $(show_key).hasClass("collapsed");
        console.log("show_key_expanded: " + show_key_expanded);
        if (show_key_expanded == true) {
            $(show_key).click();
        }
        $(".scrollspy_target").removeClass("scrollspy_target");
        $(link_selector).addClass("scrollspy_target");
        $(title_selector).addClass("scrollspy_target");
    };
}
