$("document").ready(function () {
    var div = $(".jumbotron-not-on-mobile");

    function handleResize() {
        if ($(window).width() > 600) {
            div.addClass("container");
        }
        else {
            div.removeClass("container");
        }
    }

    handleResize();
    $(window).resize(function () {
        handleResize();
    })
});