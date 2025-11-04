/**
 * TropoMetrics Email Service - Usage Examples
 * 
 * Simple examples showing how to use the email service.
 * Make sure email-service.js is included before this file.
 */

/**
 * Example 1: Send a simple email
 */
async function example1_SimpleEmail() {
    const result = await sendEmail(
        'farmer@example.com',
        'Weather Update',
        'The weather conditions have changed. Check your dashboard for details.'
    );

    if (result.success) {
        console.log('✅ Email sent successfully!');
        alert('Email sent!');
    } else {
        console.error('❌ Failed to send email:', result.message);
        alert('Failed to send email: ' + result.message);
    }
}

/**
 * Example 2: Send weather alert based on temperature
 */
async function example2_TemperatureAlert() {
    // Get current temperature from the page
    const tempElement = document.getElementById('temp-current');
    const currentTemp = parseFloat(tempElement?.textContent) || 0;

    if (currentTemp > 30) {
        const result = await sendEmail(
            'farmer@example.com',
            '🌡️ High Temperature Alert',
            `Temperature has reached ${currentTemp}°C. Consider providing shade for crops.`
        );

        if (result.success) {
            console.log('Temperature alert sent!');
        }
    }
}

/**
 * Example 3: Send watering advice
 */
async function example3_WateringAdvice() {
    // Get advice from the page
    const adviceElement = document.getElementById('advice');
    const advice = adviceElement?.textContent || '';

    if (advice.includes('Geef water')) {
        const result = await sendEmail(
            'farmer@example.com',
            '💧 TropoMetrics Watering Advice',
            `${advice}\n\nBased on current weather conditions, watering is recommended. Check your TropoMetrics dashboard for detailed information.`
        );

        if (result.success) {
            console.log('Watering advice sent!');
        }
    }
}

/**
 * Example 4: Add email button to the page
 */
function example4_AddEmailButton() {
    const headerDiv = document.querySelector('.header');
    
    const emailButton = document.createElement('button');
    emailButton.textContent = '📧 Email Report';
    emailButton.style.cssText = `
        margin-top: 10px;
        padding: 10px 20px;
        background: white;
        color: #158703;
        border: none;
        border-radius: 20px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: bold;
    `;
    
    emailButton.onclick = async () => {
        const recipient = prompt('Enter email address:');
        if (!recipient) return;

        emailButton.disabled = true;
        emailButton.textContent = '📧 Sending...';

        // Get current weather info
        const temp = document.getElementById('temp-current')?.textContent || 'N/A';
        const advice = document.getElementById('advice')?.textContent || 'N/A';
        
        const message = `
TropoMetrics Weather Report

Current Temperature: ${temp}
Advice: ${advice}

Visit your dashboard for detailed forecasts.

---
Sent from TropoMetrics Weather Service
        `.trim();

        const result = await sendEmail(
            recipient,
            '🌦️ TropoMetrics Weather Report',
            message
        );

        if (result.success) {
            alert('✅ Weather report sent successfully!');
        } else {
            alert('❌ Failed to send: ' + result.message);
        }

        emailButton.disabled = false;
        emailButton.textContent = '📧 Email Report';
    };

    headerDiv.appendChild(emailButton);
}

/**
 * Example 5: Integrate with data-weather.js
 * Add this to your existing displayAdvice function
 */
async function displayAdviceWithEmail(weather_data) {
    const advice_text = document.getElementById("advice");
    let water = false;

    const rain_data = weather_data.hourly.precipitation;
    
    for (let i = 0; i < rain_data.length; i++) {
        if (rain_data[i] > 10) {
            water = true;
        }
    }

    let adviceMessage = '';
    if (water) {
        adviceMessage = "Geef water";
        
        // Send email notification automatically
        sendEmail(
            'farmer@example.com',
            '💧 TropoMetrics: Watering Needed',
            'Based on current weather analysis, watering is recommended. Check your dashboard for complete details.'
        ).then(result => {
            if (result.success) {
                console.log('✅ Watering notification sent');
            }
        });
        
    } else {
        adviceMessage = "Water geven is nu niet nodig";
    }
    
    advice_text.textContent = adviceMessage;
}

/**
 * Example 6: Test the email service
 */
async function testEmailService() {
    console.log('🧪 Testing email service...');
    
    const testEmail = prompt('Enter your email to test:', 'test@example.com');
    if (!testEmail) return;

    const result = await sendEmail(
        testEmail,
        '✅ TropoMetrics Email Test',
        'This is a test email from TropoMetrics. If you received this, the email service is working correctly!'
    );

    if (result.success) {
        console.log('✅ Test successful! Check your email.');
        alert('Test email sent! Check your inbox.');
    } else {
        console.error('❌ Test failed:', result.message);
        alert('Test failed: ' + result.message);
    }
}

// Usage Instructions:
// 1. Include email-service.js in your HTML first
// 2. Include this file or use these examples in your own code
// 3. Call any example function or integrate into your existing code
//
// Quick test from browser console:
// testEmailService()
