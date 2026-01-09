/**
 * TropoMetrics Email Service
 * Secure email sending via backend API
 * Credentials never exposed to client
 * Includes rate limiting on email sends
 */

/**
 * Email throttler - prevents rapid successive email sends
 */
const emailThrottler = {
    lastSendTime: 0,
    minIntervalMs: 60000, // Minimum 60 seconds between emails
    
    /**
     * Check if enough time has passed since last email
     * @returns {boolean} True if send is allowed, false if throttled
     */
    isAllowed() {
        const now = Date.now();
        if (now - this.lastSendTime >= this.minIntervalMs) {
            this.lastSendTime = now;
            return true;
        }
        
        const waitSeconds = Math.ceil((this.minIntervalMs - (now - this.lastSendTime)) / 1000);
        console.warn(`🚫 Email send throttled. Wait ${waitSeconds}s before sending another email.`);
        return false;
    },
    
    /**
     * Reset throttle timer
     */
    reset() {
        this.lastSendTime = 0;
    }
};

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
    if (typeof EMAIL_CONFIG === 'undefined') {
        throw new Error('Email API not configured. Please contact administrator.');
    }
    
    // Apply rate limiting on send attempts
    if (!emailThrottler.isAllowed()) {
        throw new Error('Email send rate limited. Please wait before sending another email.');
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
            // Check for rate limit error from backend
            if (response.status === 429) {
                throw new Error('Server rate limit exceeded. Please try again later.');
            }
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
    if (typeof EMAIL_CONFIG === 'undefined') {
        return false;
    }

    try {
        const response = await fetch(`${EMAIL_CONFIG.apiUrl}/api/health`);
        return response.ok;
    } catch (error) {
        console.error('Email service health check failed:', error);
        return false;
    }
}
