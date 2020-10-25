$("document").ready(function () {
    var btn = $("#append-btn");
    var mates = btn.siblings();
    var del = btn.parent();
    var destination = del.parent();

    mates.appendTo(destination);
    btn.appendTo(destination);
    del.remove();

    var bf_input = $("#id_bf_percent");

    btn.click(function () {
        bf_input.prop('disabled', !bf_input.prop("disabled"))
            .val("");

        $("input").filter(function (indx) {
            return indx != 0 && indx != 2 && indx != 6
        })

            .each(function (indx) {
                $(this).prop("required", !$(this).prop("required"));
                if (indx != 0) {
                    $(this).val("")
                }
            })
    })
})