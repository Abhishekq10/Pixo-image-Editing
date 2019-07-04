$(document).ready(function () {
    $(".linearOptions").hide();
    $(".gridOptions").hide();
    $("#repeatLinear").hide();

    $('input[type="checkbox"]').click(function () {
        if ($(this).prop("checked") == true) {
            $("#repeatLinear").show(500);
        } else if ($(this).prop("checked") == false) {
            $("#repeatLinear").hide(500);
        }
    });

    $("#comboType").change(function () {
        var type = $(this).children("option:selected").val();
        if (type == "grid") {
            $(".linearOptions").hide(500);
            $(".gridOptions").show(500);
        } else {
            $(".linearOptions").show(500);
            $(".gridOptions").hide(500);
        }
    });
});