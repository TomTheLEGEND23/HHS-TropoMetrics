# Email Backend Setup Guide

## ✅ What's Been Set Up

Your button now sends emails using the **backend email-api service**. This is more secure because:
- ✅ Email credentials are stored on the backend (never exposed to browser)
- ✅ Backend handles SMTP connection
- ✅ Frontend just calls a secure API endpoint

## 🏗️ Architecture

```
Browser (Frontend)
    ↓ Click "Test Alert" button
    ↓ calls sendEmail()
    ↓
email-config.js (API URL: http://email-api:8000)
    ↓
email-service.js (makes HTTP POST request)
    ↓
Backend (email-api container)
    ↓ receives request
    ↓ uses credentials from .env
    ↓ connects to Gmail SMTP
    ↓
📧 Email sent to tropometrics@gmail.com
```

## 🚀 Quick Setup

### 1. Configure Gmail Credentials

Edit `.env` file:
```bash
EMAIL_SERVER=smtp.gmail.com:587
EMAIL_USERNAME=tropometrics@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
```

### 2. Get Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Enable 2-Step Verification (if not already)
3. Generate an app password for "Mail"
4. Copy the 16-character password
5. Paste it in `.env` as `EMAIL_PASSWORD`

### 3. Start the Services

```bash
docker-compose down
docker-compose up -d
```

### 4. Test the Email

1. Open http://localhost:8080
2. Wait for weather data to load
3. Click the **"Test Alert"** button
4. Check console for success message
5. Check tropometrics@gmail.com inbox

## 📝 What Each File Does

### Backend Files
- **`email-api/main.py`** - FastAPI backend that sends emails
- **`email-api/Dockerfile`** - Containerizes the Python backend
- **`.env`** - Stores email credentials (NOT committed to git)

### Frontend Files
- **`frontend/Website/code/email-config.js`** - Auto-generated at runtime with API URL
- **`frontend/Website/code/email-service.js`** - JavaScript functions to call backend
- **`frontend/Website/code/data-weather.js`** - Your button logic with `sendAdviceMail()`
- **`frontend/Website/index.html`** - Includes the email scripts

### Infrastructure
- **`docker-compose.yml`** - Runs both frontend and email-api containers
- **`frontend/docker-entrypoint.sh`** - Injects API URL into frontend at startup

## 🧪 Testing

### Test from Browser Console

```javascript
// Check if email config is loaded
console.log(EMAIL_CONFIG);

// Send a test email
await sendEmail(
    'tropometrics@gmail.com',
    'Test from Console',
    'This is a test email'
);
```

### Test the Backend Directly

```bash
# Health check
curl http://localhost:8000/health

# Send test email
curl -X POST http://localhost:8000/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "tropometrics@gmail.com",
    "subject": "Direct API Test",
    "body": "This is a test from curl",
    "html": false
  }'
```

## 🔍 Troubleshooting

### Email not sending?

1. **Check backend logs:**
   ```bash
   docker-compose logs email-api
   ```

2. **Verify credentials in .env:**
   ```bash
   cat .env
   ```

3. **Check Gmail App Password:**
   - Make sure it's 16 characters
   - No spaces
   - 2-Step Verification is enabled

4. **Test backend health:**
   ```bash
   curl http://localhost:8000/health
   ```

### "Email service not configured" error?

- The `.env` file might not be loaded
- Restart containers: `docker-compose restart`

### Button does nothing?

1. Open browser console (F12)
2. Look for error messages
3. Check if `EMAIL_CONFIG` is defined:
   ```javascript
   console.log(EMAIL_CONFIG);
   ```

### CORS errors?

- Backend allows all origins in development
- In production, update CORS settings in `email-api/main.py`

## 📧 Email Content

The button sends an email with:
- **To:** tropometrics@gmail.com
- **Subject:** "🌦️ TropoMetrics Weather Alert - [Advice]"
- **Body:** Current weather conditions including:
  - Temperature
  - Soil moisture
  - Air humidity
  - Watering advice
  - Location coordinates

## 🔒 Security

✅ **Secure:**
- Email credentials stored on backend only
- Never exposed to browser
- Environment variables injected at runtime
- HTTPS recommended for production

✅ **Git Safe:**
- `.env` is in `.gitignore`
- Only `.env.example` is committed
- No credentials in code

## 🎯 Next Steps

1. ✅ **Done:** Backend email API is working
2. ✅ **Done:** Button sends email via backend
3. 📋 **Optional:** Customize email template
4. 📋 **Optional:** Add HTML email formatting
5. 📋 **Optional:** Add more email triggers (daily reports, alerts, etc.)

## 📚 API Documentation

### POST /api/send-email

**Request:**
```json
{
  "to": "recipient@example.com",
  "subject": "Email subject",
  "body": "Email body content",
  "html": false
}
```

**Response (Success):**
```json
{
  "message": "Email sent successfully",
  "message_id": "abc123..."
}
```

**Response (Error):**
```json
{
  "detail": "Error message here"
}
```

---

**Need help?** Check the logs: `docker-compose logs -f email-api`
