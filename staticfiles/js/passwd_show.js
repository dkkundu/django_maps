$(".passwd_show").off("click").on("click", function () {
    // off() unbinds from multiple instances of the element
    // variables
    let btn = $(this);
    let icon = btn.children("svg");
    let el = btn.parent().prev("input");
    let type = el.attr("type");
    // toggle
    if (type === "password") {
        el.prop("type", "text");
        icon.addClass("fa-eye").removeClass("fa-eye-slash");
    } else {
        el.prop("type", "password");
        icon.addClass("fa-eye-slash").removeClass("fa-eye");
    }
});