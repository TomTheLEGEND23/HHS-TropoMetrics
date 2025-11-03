/**
 * TropoMetrics Email Service
 * Secure email sending via backend API
 * Credentials never exposed to client
 */

/**
 * Send an email via the backend API
 * @param {string} to - Recipient email address
 * @param {string} subject - Email subject
 * @param {string} body - Email body content
 * @param {boolean} html - Whether body is HTML (default: false)
 * @returns {Promise<Object>} Response from API
 */
async function sendEmail(to, subject, body, html = false) {
    // Check if EMAIL_CONFIG is loaded
    if (typeof EMAIL_CONFIG === 'undefined' || !EMAIL_CONFIG.apiUrl) {
        throw new Error('Email API not configured. Please contact administrator.');
    }

    try {
        const response = await fetch(`${EMAIL_CONFIG.apiUrl}/api/send-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                to: to,
                subject: subject,
                body: body,
                html: html
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to send email');
        }

        return {
            success: true,
            message: data.message
        };
    } catch (error) {
        console.error('Email sending failed:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Send a simple test email
 * @param {string} to - Recipient email address
 * @returns {Promise<Object>} Response from API
 */
async function sendTestEmail(to) {
    return await sendEmail(
        to,
        'Test Email from TropoMetrics',
        'This is a test email sent from the TropoMetrics weather dashboard.',
        false
    );
}

/**
 * Check if email service is available
 * @returns {Promise<boolean>} True if service is available
 */
async function checkEmailService() {
    if (typeof EMAIL_CONFIG === 'undefined' || !EMAIL_CONFIG.apiUrl) {
        return false;
    }

    try {
        const response = await fetch(`${EMAIL_CONFIG.apiUrl}/health`);
        return response.ok;
    } catch (error) {
        console.error('Email service health check failed:', error);
        return false;
    }
}
