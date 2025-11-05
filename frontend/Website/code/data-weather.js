/* TEST USER */
const test_user = {
    email: "klant@tropometrics.nl",
    api_key: "f7fdaa2c-d204-4083-9ca9-34d7bdec25ac",
    //latitude: 23.4162,
    //longitude: 25.6628
    //latitude: 52.012,
    //longitude: 4.380
    latitude: -5.013,
    longitude: -58.381
} 

/* Get the data */
//The request to the API
async function getData(location) {
    const coordinates = getCoordinates();

    const api_request = `https://api.open-meteo.com/v1/forecast?latitude=${encodeURIComponent(coordinates.latitude)}&longitude=${encodeURIComponent(coordinates.longitude)}&daily=temperature_2m_max,temperature_2m_min,daylight_duration&hourly=precipitation,relative_humidity_2m,soil_moisture_27_to_81cm&current=temperature_2m&timezone=Europe%2FBerlin`;

    // Get the data from the api
    const weather_response = await fetch(api_request);

    // Extract the data out of the reply
    if (!weather_response.ok) {
        // Throw error
    }

    const weather_data = await weather_response.json();
    console.log(weather_data);
    displayData(weather_data);
}


/* Display data */

function displayData(weather_data) {
    displayTempColumn(weather_data);

    displayAdvice(weather_data);

    displayRightColumn(weather_data);

    displayPrediction(weather_data);
}


function displayTempColumn(weather_data){
    // Current temp
    temp_current_text = document.getElementById("temp-current");
    temp_current_text.textContent = weather_data.current.temperature_2m + " °C";

    // Min temp
    temp_min_text = document.getElementById("temp-min");
    const temp_min_data = weather_data.daily.temperature_2m_min;
    temp_min_text.textContent = Math.min(...temp_min_data) + " °C";

    // Max temp
    temp_max_text = document.getElementById("temp-max");
    const temp_max_data = weather_data.daily.temperature_2m_max;
    temp_max_text.textContent = Math.max(...temp_max_data) + " °C";
}


function displayAdvice(weather_data){
    advice_text = document.getElementById("advice");

    let rain_data = weather_data.hourly.soil_moisture_27_to_81cm;
    let soil_moisture_27_to_81cm = rain_data[0];

    if (soil_moisture_27_to_81cm <= 0.14){
        advice_text.textContent = "Geef water";
    } else {
        advice_text.textContent = "Water geven is nu niet nodig";
    }
}


function displayRightColumn(weather_data){
    // Last rainfall
    // TODO
    soil_moisture_text = document.getElementById("soil-mosture");
    const soil_moisture_27_to_81cm = weather_data.hourly.soil_moisture_27_to_81cm;
    soil_moisture_text.textContent = soil_moisture_27_to_81cm[0]*100 + "%";
    // Humidity
    humidity_text = document.getElementById("humidity");
    const humidity_data = weather_data.hourly.relative_humidity_2m;
    humidity_text.textContent = humidity_data[0] + "%";

    // Solar hours
    solar_text = document.getElementById("solar-hours");
    const solar_data = weather_data.daily.daylight_duration;
    solar_text.textContent = Math.round(solar_data[0] / 3600) + " uur en " + Math.round((solar_data[0] % 3600) / 60) + " minuten.";
}


function displayPrediction(weather_data){
    const precipitationGrid = document.getElementById('precipitation-grid');

    const date = new Date();
    let time_hour = date.getHours();

    if (time_hour > 0){
        const rest = time_hour % 6;
        time_hour -= rest;
    }

    const time_line_graph = 24 * 5 + time_hour;

    if (weather_data.hourly.length < time_line_graph){
        // Error
    }

    let precipitation_5days = [];
    let amount = 0;
    let max_precipitation = 0.1;
    for (let i = time_hour; i < time_line_graph; i++) {
        amount += weather_data.hourly.precipitation[i];

        if ((i % 6) == 0 && i != 0){
            precipitation_5days.push(amount);
            if (max_precipitation < amount){
                max_precipitation = amount;
            }
            amount = 0;
        }        
    }

    if (max_precipitation < 1){
        max_precipitation *= 2;
    } else {
        max_precipitation += 2;
    }

    // Implement y-axis
    const precipitation_text_max = document.getElementById('max-precipitation');
    precipitation_text_max.textContent = max_precipitation + "mm";
    const precipitation_text_middle = document.getElementById('middle-precipitation');
    precipitation_text_middle.textContent = max_precipitation/2 + "mm";

    let day_counter = date.getDate();
    month_bar = date.getMonth();
    // Implement bars
    for (let i = 0; i < precipitation_5days.length; i++){
        let height_bar = precipitation_5days[i] * 200 / max_precipitation;

        const precipitation_bar = document.createElement('div');
        precipitation_bar.className = 'bar-histogram';
        precipitation_bar.style = "height: " + height_bar +"px;";
        precipitation_bar.title = day_counter + "/" + (month_bar+1) + " - " + time_hour + ": " + precipitation_5days[i] + "mm";

        precipitationGrid.appendChild(precipitation_bar);

        time_hour = (time_hour + 6) % 24;
        
        if (time_hour == 0){
            day_counter++;

            const day_divider_container = document.createElement('div');
            day_divider_container.className = 'day-divider-container';
            
            const day_divider = document.createElement('div');
            day_divider.className = 'day-divider';
            
            const day_label = document.createElement('div');
            day_label.className = 'day-label';
            day_label.textContent = day_counter + '/' + (month_bar + 1);
            
            day_divider_container.appendChild(day_divider);
            day_divider_container.appendChild(day_label);
            precipitationGrid.appendChild(day_divider_container);            
        }
    }
}


function getCoordinates(){
    const coordinates = {
        latitude: test_user.latitude,
        longitude: test_user.longitude
    }

    return coordinates;
}


 document.addEventListener('DOMContentLoaded', function() {
    const alert_button = document.getElementById('alert-button');

    // Search button click
    alert_button.addEventListener('click', function() {
        // Code for the email
        sendAdviceMail();
    });
 });


async function sendAdviceMail(){
    // Get advice from the page
    const adviceElement = document.getElementById('advice');
    const advice = adviceElement?.textContent || '';
    
    console.log("📧 Sending email notification...");

    // Get current weather data for the email
    const temp = document.getElementById('temp-current')?.textContent || 'N/A';
    const soilMoisture = document.getElementById('soil-mosture')?.textContent || 'N/A';
    const humidity = document.getElementById('humidity')?.textContent || 'N/A';

    // Create email body with weather information
    const emailBody = `
TropoMetrics Weather Alert

Current Conditions:
- Temperature: ${temp}
- Soil Moisture: ${soilMoisture}
- Air Humidity: ${humidity}

Advice: ${advice}

${advice.includes('Geef water') ? 'Based on current weather conditions, watering is recommended.' : 'No watering needed at this time.'}

Check your TropoMetrics dashboard for detailed information and forecasts.

---
This is an automated message from TropoMetrics Weather Service
Location: Lat ${test_user.latitude}, Lon ${test_user.longitude}
    `.trim();

    try {
        const result = await sendEmail(
            'tropometrics@gmail.com',
            '🌦️ TropoMetrics Weather Alert - ' + advice,
            emailBody,
            false  // plain text email
        );

        if (result.success) {
            console.log('✅ Email sent successfully!');
            alert('✅ Weather alert sent to tropometrics@gmail.com');
        } else {
            console.error('❌ Failed to send email:', result.error);
            alert('❌ Failed to send email: ' + result.error);
        }
    } catch (error) {
        console.error('❌ Error sending email:', error);
        alert('❌ Error sending email. Check console for details.');
    }
}

getData();