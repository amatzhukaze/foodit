var imageurl = "";
// XHR and keep URL
$(document).ready(function() {

    $("form[name=add-form]").submit(function(event) {
        event.preventDefault();
        var data = $("form[name=add-form]").serializeArray();
        var output = {};
        for (i=0; i < data.length; i++) {
            output[data[i].name] = data[i].value;
        }
        $.ajax({
            type: "POST",
            url: $("form[name=add-form]").attr("action"),
            data: output,
            dataType: "json",
            success: function(data) {
                console.log(data);
            }
        })
    })
});

// Convert serialized array to cleaner JSON format, and add image url, send XHR