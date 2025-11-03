/* Get the data */
//The request to the API
async function getData(location) {
    const coordinates = getCoordinates();

    const api_request = `https://api.open-meteo.com/v1/forecast?latitude=${encodeURIComponent(coordinates.latitude)}&longitude=${encodeURIComponent(coordinates.longitude)}&daily=temperature_2m_max,temperature_2m_min,daylight_duration&hourly=precipitation,relative_humidity_2m&current=temperature_2m`;

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
    water = false;

    rain_data = weather_data.hourly.precipitation;
    let rain_data_length = rain_data.length;

    // Logic for the advice
    // TODO uitbreiden
    for (let i = 0; i < rain_data_length; i++){
        if (rain_data[i] > 10){
            water = true;
        }
    }

    if (water){
        advice_text.textContent = "Geef water";
    } else {
        advice_text.textContent = "Water geven is nu niet nodig";
    }
}


function displayRightColumn(weather_data){
    // Last rainfall
    // TODO

    // Humidity
    humidity_text = document.getElementById("humidity");
    const humidity_data = weather_data.hourly.relative_humidity_2m;
    humidity_text.textContent = humidity_data[0] + "%";

    // Solar hours
    solar_text = document.getElementById("solar-hours");
    const solar_data = weather_data.daily.daylight_duration;
    solar_text.textContent = Math.round(solar_data[0] / 3600) + " uur en " + Math.round((solar_data[0] % 3600) / 60) + " minuten.";
}


function getCoordinates(){
    const coordinates = {
        latitude: 52.012,
        longitude: 4.380
    }

    return coordinates;
}


// Get forcast data
let coordinates = 

getData();
