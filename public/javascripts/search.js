$(document).ready(function() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            $("input[name='lat']").attr('value', position.coords.latitude);
            $("input[name='lon']").attr('value', position.coords.longitude);
        }, function(error) {
            console.error(error);
            // Use IP address
        });
    } else {
        // Use IP Address
        console.log("lol");
    }
})