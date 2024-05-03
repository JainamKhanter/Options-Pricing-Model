//script.js

$(document).ready(function () {
    $("#calculate-btn").click(function () {
      function daysFromCurrentDate(inputDate) {
        var dateError = $("#dateError");
        var currentDate = new Date();
        var inputDateObject = new Date(inputDate);
        var duration = inputDateObject.getTime() - currentDate.getTime();
        //if(duration<=0) {dateError.textContent = "Invalid Date";dateError.show()
        //return;}
        return Math.ceil(duration / (1000 * 3600 * 24));
      }

      function updateImageSrc(imageSrc) {
        var imgElement = document.getElementById('plot');
        imgElement.src = imageSrc;
      }

  
      var data = {
        //underlyingPrice: parseFloat(10000),
        company: document.getElementById("company_name").value,
        //   strikePrice: parseFloat(document.getElementById("strike price").value),
        daysUntilExpiration: parseFloat(
          daysFromCurrentDate(document.getElementById("duration").value)
        ),
        interestRate: parseFloat(7),
        //volatility: parseFloat(10),
        dividendYield: parseFloat(2),
      };
  
      $.ajax({
        url: "http://localhost:5000/monte_carlo",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
  
        success: function (response) {
        //   document.getElementById("plot").value
        //   Thread.sleep(10)
          updateImageSrc(response['plot_filename'])
          console.log("Graph displayed successfully");
        },
        error: function (xhr, status, error) {
          console.log(data);
          console.error("Error:", error);
        },
      });
    });
  });