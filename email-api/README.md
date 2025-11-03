# TropoMetrics Email API

Secure backend API for sending emails via SMTP. Credentials stored as Kubernetes secrets, never exposed to client.

## Architecture

```
Frontend (Browser) → Email API (K8s Pod) → SMTP Server (Gmail)
  (public)              (has secrets)         (external)
```

**Security**: Email credentials (username, password, server) are:
- ✅ Stored in Kubernetes Secrets
- ✅ Injected into email-api pods only
- ✅ Never sent to browser/frontend
- ✅ Never committed to Git

## API Endpoints

### `GET /`
Health check endpoint
```json
{
  "service": "TropoMetrics Email API",
  "status": "healthy",
  "configured": true
}
```

### `GET /health`
Kubernetes readiness/liveness probe
```json
{"status": "ok"}
```

### `POST /api/send-email`
Send an email via SMTP

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
  "status": "success",
  "message": "Email sent to recipient@example.com"
}
```

**Response (Error):**
```json
{
  "detail": "Error message"
}
```

## Frontend Usage

```javascript
// Include scripts in HTML
<script src="code/email-config.js"></script>
<script src="code/email-service.js"></script>

// Send email
const result = await sendEmail(
    'user@example.com',
    'Weather Alert',
    'High rainfall expected!'
);

if (result.success) {
    console.log('Email sent!');
} else {
    console.error('Failed:', result.error);
}

// Check service health
const isAvailable = await checkEmailService();
```

## Local Development

```bash
cd email-api

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export EMAIL_USERNAME="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export EMAIL_SERVER="smtp.gmail.com:587"

# Run locally
python main.py

# Test API
curl http://localhost:8000/health
```

## Docker Build

```bash
cd email-api
docker build -t tropometrics-email-api .
docker run -p 8000:8000 \
  -e EMAIL_USERNAME="your-email@gmail.com" \
  -e EMAIL_PASSWORD="your-app-password" \
  -e EMAIL_SERVER="smtp.gmail.com:587" \
  tropometrics-email-api
```

## Kubernetes Deployment

The email API is automatically deployed alongside the frontend:
- **Production**: 2 replicas, included in `k8s/main-env.yaml`
- **Development**: 1 replica, included in `k8s/dev-env.yaml`

Service endpoints:
- **Internal**: `http://tropometrics-email-api-service:8000`
- **Frontend access**: Via `EMAIL_CONFIG.apiUrl` environment variable

## Testing

Visit the test page after deployment:
- Production: `http://10.0.0.101:30080/email-test.html`
- Development: `http://10.0.0.101:30081/email-test.html`

## Dependencies

- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **smtplib**: Built-in Python SMTP client

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_USERNAME` | SMTP username (email address) | `user@gmail.com` |
| `EMAIL_PASSWORD` | SMTP password (Gmail App Password) | `abcd efgh ijkl mnop` |
| `EMAIL_SERVER` | SMTP server and port | `smtp.gmail.com:587` |

All injected from Kubernetes Secret `tropometrics-email-secrets`
