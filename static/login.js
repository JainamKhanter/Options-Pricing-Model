$(document).ready(function() {
    $('#login-form').submit(function(event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        // var csrf_token = $('input[name="csrf_token"]').val();

        $.ajax({
            url: '/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({username: username, password: password, csrf_token: csrf_token}),
            success: function(response) {
                console.log('Login successful');
                window.location.href = '/dashboard'; // Redirect to dashboard on successful login
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                $('#error-message').text('Invalid username or password');
            }
        });
    });
});