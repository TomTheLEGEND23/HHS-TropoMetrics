/**
 * TropoMetrics Email Service - Simple Client-Side Email
 * 
 * This uses EmailJS service (https://www.emailjs.com/) to send emails directly from the browser.
 * EmailJS provides a free tier: 200 emails/month
 * 
 * SETUP:
 * 1. Sign up at https://www.emailjs.com/
 * 2. Add Gmail service and verify your email
 * 3. Create an email template
 * 4. Get your Public Key, Service ID, and Template ID
 * 5. Update the credentials in email-config.js
 * 
 * NOTE: Configuration is loaded from email-config.js
 * Make sure to include email-config.js BEFORE this file in your HTML
 */

/**
 * Initialize EmailJS (loads the library if not already loaded)
 */
async function initEmailJS() {
    // Check if config is loaded
    if (typeof window.EMAIL_CONFIG === 'undefined') {
        throw new Error('Email configuration not loaded. Make sure to include email-config.js before email-service.js');
    }

    if (typeof emailjs !== 'undefined') {
        return; // Already loaded
    }
    
    // Load EmailJS library
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js';
        script.onload = () => {
            emailjs.init(window.EMAIL_CONFIG.publicKey);
            resolve();
        };
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

/**
 * Send an email using EmailJS
 * @param {string} to - Recipient email address
 * @param {string} subject - Email subject
 * @param {string} message - Email message/text
 * @returns {Promise<Object>} Response object with success status
 */
async function sendEmail(to, subject, message) {
    try {
        // Validate inputs
        if (!to || !subject || !message) {
            throw new Error('Missing required fields: to, subject, and message are required');
        }

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(to)) {
            throw new Error('Invalid email address format');
        }

        console.log('📧 Sending email to:', to);

        // Initialize EmailJS
        await initEmailJS();

        // Send email via EmailJS
        const templateParams = {
            to_email: to,
            subject: subject,
            message: message,
            from_name: 'TropoMetrics Weather Service'
        };

        const response = await emailjs.send(
            window.EMAIL_CONFIG.serviceId,
            window.EMAIL_CONFIG.templateId,
            templateParams
        );

        console.log('✅ Email sent successfully:', response);

        return {
            success: true,
            message: 'Email sent successfully',
            data: response
        };

    } catch (error) {
        console.error('❌ Email sending failed:', error);
        
        return {
            success: false,
            message: error.message || 'Failed to send email',
            error: error.text || error.message
        };
    }
}

// Make function available globally
window.sendEmail = sendEmail;
