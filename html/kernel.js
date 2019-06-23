// Main
$(document).ready(function(){
    var getData = function (request, response) {
        var url = "http://127.0.0.1:8080/symbols/" + request.term
        $.getJSON(
            url + "?callback=?",
            function (data) {
                response(data.symbols);
            });
    };

    var selectItem = function (event, ui) {
        $("#selected_option").text(ui.item.value);
        return false;
    }

    $("#autocomplete").autocomplete({
        source: getData,
        select: selectItem,
        minLength: 4,
        change: function() {
            $("#autocomplete").val("").css("display", 2);
        }
    });
});
