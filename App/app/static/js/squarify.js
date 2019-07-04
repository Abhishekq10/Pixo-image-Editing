
$(document).ready(function(){
    var stype;
    var marginVal = 0;
    $("#section2").hide();
    $("#typeSelect").change(function(){
        
        $("#section2").toggle(500);
    });

    $("#proceed1").on("click", function(){
        marginVal = $("#MarginPer").val();
        stype = $("#typeSelect").children("option:selected").val();
        console.log(stype);
        console.log(marginVal);
        var height = $("#aspectHeight").val();
        var width = $("#aspectWidth").val();
        console.log(width + ":" + height);
    });

});