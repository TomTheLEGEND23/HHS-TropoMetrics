# Email API Usage Guide

## Overview

The TropoMetrics Email API is a secure backend service that handles email sending for the frontend application. Email credentials (SMTP username, password, server) are stored as **Kubernetes secrets** and **never exposed to the client**, ensuring security and preventing credential theft.

## Architecture

```
Frontend (Browser)  →  Email API (Backend)  →  SMTP Server  →  Recipient
   HTML/JS              FastAPI (Python)         Gmail/etc
```

- **Frontend**: Calls API via JavaScript
- **Backend**: Handles SMTP authentication securely
- **Secrets**: Stored in Kubernetes, injected as environment variables

## API Endpoints

### 1. Health Check
```
GET /health
```
Returns the health status of the email service.

**Response:**
```json
{
  "status": "healthy",
  "service": "TropoMetrics Email API"
}
```

### 2. Send Email
```
POST /api/send-email
```
Sends an email to a specified recipient.

**Request Body:**
```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": "Email body content",
  "html": false
}
```

**Parameters:**
- `to` (string, required): Recipient email address (validated)
- `subject` (string, required): Email subject line
- `body` (string, required): Email body content (plain text or HTML)
- `html` (boolean, optional): Set to `true` for HTML emails, `false` for plain text (default: `false`)

**Success Response (200):**
```json
{
  "message": "Email sent successfully",
  "to": "recipient@example.com"
}
```

**Error Response (500):**
```json
{
  "detail": "Failed to send email: [error message]"
}
```

## Frontend JavaScript Usage

### Including the Email Service

Add the email service script to your HTML:

```html
<script src="code/email-service.js"></script>
```

### Basic Functions

#### 1. Send Simple Email
```javascript
// Send a plain text email
const result = await sendEmail(
    'recipient@example.com',
    'Hello from TropoMetrics',
    'This is the email body content.',
    false  // plain text
);

if (result.success) {
    console.log('Email sent:', result.message);
} else {
    console.error('Email failed:', result.error);
}
```

#### 2. Send HTML Email
```javascript
// Send an HTML formatted email
const htmlContent = `
    <h1>Weather Alert</h1>
    <p>Current temperature: <strong>25°C</strong></p>
    <p>Visit our <a href="https://example.com">dashboard</a> for more.</p>
`;

const result = await sendEmail(
    'user@example.com',
    'Weather Update',
    htmlContent,
    true  // HTML format
);
```

#### 3. Send Test Email
```javascript
// Quick test email function
const result = await sendTestEmail('test@example.com');
console.log(result);
```

#### 4. Check Service Availability
```javascript
// Check if email service is running
const isAvailable = await checkEmailService();
if (isAvailable) {
    console.log('Email service is ready');
} else {
    console.log('Email service unavailable');
}
```

### Complete Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>Email Example</title>
</head>
<body>
    <h1>Send Email</h1>
    <form id="emailForm">
        <input type="email" id="recipient" placeholder="Recipient" required>
        <input type="text" id="subject" placeholder="Subject" required>
        <textarea id="body" placeholder="Message" required></textarea>
        <label>
            <input type="checkbox" id="isHtml"> HTML Format
        </label>
        <button type="submit">Send Email</button>
    </form>
    <div id="result"></div>

    <script src="code/email-service.js"></script>
    <script>
        document.getElementById('emailForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const to = document.getElementById('recipient').value;
            const subject = document.getElementById('subject').value;
            const body = document.getElementById('body').value;
            const html = document.getElementById('isHtml').checked;
            
            const result = await sendEmail(to, subject, body, html);
            
            const resultDiv = document.getElementById('result');
            if (result.success) {
                resultDiv.innerHTML = `<p style="color: green;">✓ ${result.message}</p>`;
            } else {
                resultDiv.innerHTML = `<p style="color: red;">✗ Error: ${result.error}</p>`;
            }
        });

        // Check service on page load
        checkEmailService().then(available => {
            if (!available) {
                alert('Email service is currently unavailable');
            }
        });
    </script>
</body>
</html>
```

## Configuration

### Environment Variables (Kubernetes)

The email API requires these environment variables (injected from K8s secrets):

```yaml
env:
- name: EMAIL_USERNAME
  valueFrom:
    secretKeyRef:
      name: tropometrics-email-secrets
      key: Email-Username
- name: EMAIL_PASSWORD
  valueFrom:
    secretKeyRef:
      name: tropometrics-email-secrets
      key: Email-Password
- name: EMAIL_SERVER
  valueFrom:
    secretKeyRef:
      name: tropometrics-email-secrets
      key: Email-Server
```

### Frontend Configuration

The frontend automatically receives the email API URL via environment variable injection:

```javascript
// Automatically loaded by docker-entrypoint.sh
window.EMAIL_CONFIG = {
    apiUrl: 'http://tropometrics-email-api-service:8000'  // K8s DNS
};
```

## Security Features

✅ **Credentials Never Exposed**: SMTP credentials stored only in Kubernetes secrets  
✅ **Backend Authentication**: All SMTP communication happens server-side  
✅ **CORS Protection**: API configured to accept requests only from trusted origins  
✅ **Email Validation**: Recipient addresses validated before sending  
✅ **Error Handling**: Detailed errors logged server-side, generic errors sent to client  

## Error Handling

### Common Errors

**1. "Email API not configured"**
- **Cause**: `EMAIL_CONFIG` not loaded
- **Solution**: Ensure `docker-entrypoint.sh` is injecting the config

**2. "Failed to send email"**
- **Cause**: SMTP authentication failed or network issue
- **Solution**: Check K8s secrets and SMTP server credentials

**3. "Email service health check failed"**
- **Cause**: Backend API not reachable
- **Solution**: Verify email-api pod is running: `kubectl get pods -n tropometrics`

### Debugging

```javascript
// Enable console logging
sendEmail('test@example.com', 'Test', 'Body', false)
    .then(result => console.log('Success:', result))
    .catch(error => console.error('Failed:', error));

// Check API health
fetch('http://tropometrics-email-api-service:8000/health')
    .then(r => r.json())
    .then(data => console.log('API Status:', data))
    .catch(err => console.error('API Unreachable:', err));
```

## SMTP Server Configuration

### Gmail Example
```
Email-Server: smtp.gmail.com:587
Email-Username: your-email@gmail.com
Email-Password: your-app-password  # Use App Password, not regular password
```

### Other Providers
- **Outlook**: `smtp.office365.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: `your-smtp-server.com:587`

## Testing

### Test Email Endpoint
```bash
# Using curl
curl -X POST http://10.0.0.101:8000/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "Test Email",
    "body": "This is a test.",
    "html": false
  }'
```

### Frontend Test Page
Open `Website/email-test.html` in your browser for a built-in test interface.

## Troubleshooting

### Email Not Sending

1. **Check API Health**:
   ```bash
   kubectl logs -n tropometrics -l app=tropometrics-email-api
   ```

2. **Verify Secrets**:
   ```bash
   kubectl get secret tropometrics-email-secrets -n tropometrics -o yaml
   ```

3. **Test SMTP Manually**:
   ```bash
   kubectl exec -it <email-api-pod> -n tropometrics -- python3 -c "
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('user@gmail.com', 'password')
   print('SMTP OK')
   "
   ```

### CORS Issues

If getting CORS errors in browser console:
1. Check email API logs for blocked origins
2. Update `allow_origins` in `email-api/main.py` if needed
3. Ensure frontend is served from expected domain

## Best Practices

1. ✅ Always check `result.success` before showing success message
2. ✅ Validate email addresses client-side before sending
3. ✅ Show loading states during email sending
4. ✅ Provide user feedback for both success and failure
5. ✅ Don't expose sensitive information in error messages
6. ✅ Rate limit email sending if implementing contact forms
7. ✅ Use HTML emails sparingly (prefer plain text for security)

## Production Considerations

- Configure specific CORS origins (not `*`)
- Implement rate limiting to prevent spam
- Add email queue for bulk sending
- Monitor API logs for failed sends
- Set up alerts for authentication failures
- Consider using email service providers (SendGrid, Mailgun) for better deliverability
- Implement email templates for consistent formatting
- Add email validation/verification for important messages

## Support

For issues or questions:
- Check logs: `kubectl logs -n tropometrics <pod-name>`
- Review secrets: `kubectl describe secret tropometrics-email-secrets -n tropometrics`
- Test API: `curl http://10.0.0.101:8000/health`
