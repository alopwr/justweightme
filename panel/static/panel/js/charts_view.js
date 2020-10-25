$("document").ready(function () {
    var diff_input = $("#id_different");

    function handleHiddenInput() {
        if ($("#id_chart_type option:selected").val() === "inny") {
            diff_input.show()
                .attr("required", true);
        }
        else {
            diff_input.attr("required", false)
                .hide();
        }
    }

    handleHiddenInput();

    $("#id_chart_type").change(function () {
        handleHiddenInput()
    })
});