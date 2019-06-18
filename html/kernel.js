// Main
$(document).ready(function(){
    $.ajax({
           url: "http://jsonplaceholder.typicode.com/users",
           async: true,
           dataType: 'json',
           success: function (data) {
               var arrayReturn = [];
               for (var i = 0, len = data.length; i < len; i++) {
                   var id = (data[i].id).toString();
                   arrayReturn.push({'value' : data[i].name, 'data' : id});
               }
               loadSuggestions(arrayReturn);
           }
    });
    function loadSuggestions(options) {
        $('#autocomplete').autocomplete({
                                        lookup: options,
                                        onSelect: function (suggestion) {
                                            $('#selected_option').html(suggestion.value);
                                        }
        });
    }
});
