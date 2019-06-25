// Main
$(document).ready(function(){
    // Search
    var getData = function (request, response) {
        var url = "http://127.0.0.1:8080/symbols/" + request.term;
        $.getJSON(
            url + "?callback=?",
            function (data) {
                response(data.symbols);
            }
        );
    }

    var selectItem = function (event, ui) {
        $("#selected_option").text(ui.item.value);
        return false;
    }

    $("#autocomplete").autocomplete({
        source: getData,
        select: selectItem,
        minLength: 4,
    });


    // Details
    var hashChanged = function(window_hash) {
        symbol = window_hash.substr(1);
        $("#details").text(symbol);
    }
    hashChanged(window.location.hash); // initial value

    // updates (based upon https://stackoverflow.com/a/2162174)
    if ("onhashchange" in window) { // event supported?
        window.onhashchange = function () {
            hashChanged(window.location.hash);
        }
    }
    else { // event not supported:
        var storedHash = window.location.hash;
        window.setInterval(function () {
            if (window.location.hash != storedHash) {
                storedHash = window.location.hash;
                hashChanged(storedHash);
            }
        }, 100);
    }
});
