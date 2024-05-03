
const dates = [];
const opens = [];
const highs = [];
const lows = [];
const closes = [];
const volumes = [];
const counts = [];


const fs = require('fs');
const csv = require('csv-parser');

const results = {};

fs.createReadStream('BSE.csv')
  .pipe(csv())
  .on('data', (data) => {
    results[data['tradingsymbol']] = data['instrument_key'];
    
  })
  .on('end', () => {
   
    console.log(results['AARTIIND']);


const xyz = results['AARTIIND'];
fetch(`https://api.upstox.com/v2/historical-candle/${xyz}/day/2024-04-26/2024-04-19`
, {
  method: 'GET',
  headers: {
    'Accept': 'application/json'
  }
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  
  return response.json();
})
.then(data => {
  
  console.log(data);
  console.log(data.data.candles);
  
    data.data.candles.forEach(candle => {
    dates.push(candle[0]);
    opens.push(candle[1]);
    highs.push(candle[2]);
    lows.push(candle[3]);
    closes.push(candle[4]);
    volumes.push(candle[5]);
    counts.push(candle[6]);    
  });

  console.log("Dates:", dates);
console.log("Opens:", opens);
console.log("Highs:", highs);
console.log("Lows:", lows);
console.log("Closes:", closes);
console.log("Volumes:", volumes);
console.log("Counts:", counts);

const returns = [];
for (let i = 1; i < closes.length; i++) {
  const prevClose = closes[i - 1];
  const currentClose = closes[i];
  const logReturn = Math.log(currentClose / prevClose);
  returns.push(logReturn);
}

// Calculate standard deviation of returns
const meanReturn = returns.reduce((sum, val) => sum + val, 0) / returns.length;
const squaredDifferences = returns.map(val => Math.pow(val - meanReturn, 2));
const variance = squaredDifferences.reduce((sum, val) => sum + val, 0) / returns.length;
const v = Math.sqrt(variance);
})
.catch(error => {  
  console.error('There was a problem with your fetch operation:', error);
});

  });


 
  
  
  










