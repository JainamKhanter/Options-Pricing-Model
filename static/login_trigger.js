$(document).ready(function() {
    $('#login-btn').click(function() {
        $.ajax({
            url: 'http://localhost:5000/login',
            type: 'GET',
            success: function(response) {
                // Handle successful response from the server
                console.log(response);
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error('Error:', error);
            }
        });
    });
});
