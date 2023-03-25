$(document).ready(function() {
    $("#contact-form").submit(function(event) {
        event.preventDefault(); // prevent form from submitting via browser

        var name = $("#name").val();
        var email = $("#email").val();
        var phone = $("#phone").val();
        var message = $("#message").val();

        // send form data to Flask app
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/contact",
            data: {
                name: name,
                email: email,
                phone: phone,
                message: message
            },
            success: function(response) {
                // Update message element with response from Flask app
                $("#popup-message").text(response.confirmation_message).dialog();
                // reset the form
                $("#contact-form")[0].reset();
            },
            error: function() {
                // Handle any errors that occur
                $("#popup-message").text("Sorry, an error occurred while submitting the form. Please try again later.").dialog();
            }
        });
    });
});
