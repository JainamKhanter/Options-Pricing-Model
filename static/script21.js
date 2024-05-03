// script.js

$(document).ready(function() {
    $('#calculate-btn').click(function() {
        function
daysFromCurrentDate(inputDate){
    var dateError = $("#dateError");
    var currentDate = new Date();
    var inputDateObject = new Date(inputDate);
    var duration = inputDateObject.getTime()-currentDate.getTime();
    //if(duration<=0) {dateError.textContent = "Invalid Date";dateError.show()
    //return;}
    return Math.ceil(duration/(1000*3600*24));
}
        var data = {
            underlyingPrice: parseFloat(document.getElementById('option price').value),
            strikePrice: parseFloat(document.getElementById('strike price').value),
            daysUntilExpiration: parseFloat(daysFromCurrentDate(document.getElementById('duration').value)),
            interestRate: parseFloat(document.getElementById('rate').value),
            volatility: parseFloat(document.getElementById('volatality').value),
            dividendYield: parseFloat(document.getElementById('yield').value),
            
        };

        $.ajax({
            url: 'http://localhost:5000/calculate1',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                console.log('Black-Scholes Call Price:', response['call']);
                console.log('Black-Scholes Put Price:', response['put']);
                console.log('Black-Scholes Call Delta:', response['call_delta']);
                console.log('Black-Scholes Put Delta:', response['put_delta']);
                console.log('Black-Scholes Call Theta:', response['call_theta']);
                console.log('Black-Scholes Put Theta:', response['put_theta']);
                console.log('Black-Scholes Call Rho:', response['call_rho']);
                console.log('Black-Scholes Put Rho:', response['put_rho']);
                console.log('Black-Scholes Gamma:', response['gamma']);
                console.log('Black-Scholes Vega:', response['vega']);
                // Update HTML elements with the calculated values
                document.getElementById('call-price').innerText = response['call'].toFixed(4);
                document.getElementById('put-price').innerText = response['put'].toFixed(4);
                document.getElementById('call-delta').innerText = response['call_delta'].toFixed(4);
                document.getElementById('put-delta').innerText = response['put_delta'].toFixed(4);
                document.getElementById('call-theta').innerText = response['call_theta'].toFixed(4);
                document.getElementById('put-theta').innerText = response['put_theta'].toFixed(4);
                document.getElementById('call-rho').innerText = response['call_rho'].toFixed(4);
                document.getElementById('put-rho').innerText = response['put_rho'].toFixed(4);
                document.getElementById('gamma').innerText = response['gamma'].toFixed(4);
                document.getElementById('vega').innerText = response['vega'].toFixed(4);
                
                // Update your HTML elements with the calculated values
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
