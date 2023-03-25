$(document).ready(function() {
    $('#upload-file').submit(function(event) {
        event.preventDefault();
        handleFileUpload();
    });
});


function handleFileUpload() {
    const input = document.querySelector('input[type="file"]');
    const file = input.files[0];

    // Check if file is TXT
    if (file.type === "text/plain") {
        // Read file content and convert to text
        const reader = new FileReader();
        reader.readAsText(file, 'UTF-8');
        reader.onload = function (evt) {
            const text = evt.target.result; 
            // Send text to server for classification
            $.ajax({
                url: 'http://127.0.0.1:5000/summarize',
                type: 'POST',
                data: {text: text},
                success: function(response) {
                    $("#result").html(response.summary);
                    $("#upload-file")[0].reset();
                },
                error: function() {
                    // Handle any errors that occur
                    $("#result").text("Sorry, an error occurred while uploading the file. Please try again later.");
                }
            });
        }
        reader.onerror = function (evt) {
            console.error(evt);
        }
    } else {
        $("#result").text("Invalid file type. Please upload a TXT file only.");
        $("#upload-file")[0].reset();
    }
}
