const fetch = require('node-fetch');

exports.handler = async function(event, context) {
  const API_URL = 'https://corsproxy.io/?https%3A%2F%2Fjustmysocks5.net%2Fmembers%2Fgetbwcounter.php%3Fservice%3D531532%26id%3D0ffb1cda-1854-43ec-88c2-8d63cd32f280';

  try {
    // Fetch the API data
    const response = await fetch(API_URL);
    const data = await response.json();

    // Get the data from the API response
    const monthlyBwLimit = data.monthly_bw_limit_b;
    const bwCounter = data.bw_counter_b;
    const bwResetDayOfMonth = data.bw_reset_day_of_month;

    // Read the file you want to return (e.g., mcca.yaml)
    const fileContent = await readFileFunction('path_to_mcca.yaml'); // You'll need to define or import a readFile function

    // Return the file with the headers
    return {
      statusCode: 200,
      headers: {
        'Content-Disposition': 'attachment; filename=mcca.yaml',
        'X-Monthly-BW-Limit': monthlyBwLimit.toString(),
        'X-BW-Counter': bwCounter.toString(),
        'X-BW-Reset-Day-Of-Month': bwResetDayOfMonth.toString(),
        'Content-Type': 'application/octet-stream'
      },
      body: fileContent
    };

  } catch (error) {
    return {
      statusCode: 500,
      body: `Error fetching data: ${error.message}`
    };
  }
};
