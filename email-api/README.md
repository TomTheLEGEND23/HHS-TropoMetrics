# TropoMetrics Email API

Secure backend API for sending emails via SMTP. Credentials stored as Kubernetes secrets, never exposed to client.

## Architecture

```
Browser → Frontend (Port 30080/30081)
  ↓ loads email-config.js with EMAIL_API_URL
  ↓
Browser → Email API (Port 30090/30091) → SMTP Server (Gmail)
          (exposed NodePort)              (external)
          (has secrets)
```

**Direct Access**: Browser makes API calls directly to the email backend exposed via NodePort.

**Security**: Email credentials (username, password, server) are:
- ✅ Stored in Kubernetes Secrets
- ✅ Injected into email-api pods only
- ✅ Never sent to browser/frontend
- ✅ Never committed to Git

**Port Assignments:**
- Production (main): Frontend 30080, Email API 30090
- Development (dev): Frontend 30081, Email API 30091

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

### Service Endpoints

| Environment | Internal Service | External NodePort |
|------------|------------------|-------------------|
| Production | `tropometrics-email-api-service:8000` | `http://10.0.0.101:30090` |
| Development | `tropometrics-email-api-service:8000` | `http://10.0.0.101:30091` |

**Frontend Configuration:**
- Environment variable `EMAIL_API_URL` is injected at runtime
- `docker-entrypoint.sh` creates `email-config.js` with the correct API URL
- Browser JavaScript uses this URL to make direct API calls

## Testing

### Web Interface
Visit the test page after deployment:
- Production: `http://10.0.0.101:30080/email-test.html`
- Development: `http://10.0.0.101:30081/email-test.html`

### Direct API Testing

**Health Check:**
```bash
# Production
curl http://10.0.0.101:30090/health

# Development  
curl http://10.0.0.101:30091/health
```

**Send Test Email:**
```bash
# Development
curl -X POST http://10.0.0.101:30091/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "your-email@example.com",
    "subject": "Test from TropoMetrics",
    "body": "This is a test email from the development environment!",
    "html": false
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Email sent to your-email@example.com"
}

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

## Troubleshooting

### Email service not available (404 error)

Check if the email API pod is running:
```bash
kubectl get pods -n tropometrics | grep email-api
```

Check the service is exposed:
```bash
kubectl get svc -n tropometrics | grep email-api
```

### Authentication Failed (401 error)

For Gmail, ensure you're using an **App Password**, not your regular password:
1. Enable 2-Factor Authentication
2. Generate App Password at https://myaccount.google.com/apppasswords
3. Update the Kubernetes secret with the 16-character password

### Check Pod Logs

```bash
# Get pod name
kubectl get pods -n tropometrics -l app=tropometrics-email-api

# View logs
kubectl logs -n tropometrics <pod-name>
```

### Verify Secrets

```bash
# Check secret exists
kubectl get secret tropometrics-email-secrets -n tropometrics

# View secret keys (values are base64 encoded)
kubectl describe secret tropometrics-email-secrets -n tropometrics
```

### Test from inside the cluster

```bash
# Get a shell in the frontend pod
kubectl exec -it -n tropometrics <frontend-pod-name> -- sh

# Test email API from inside
wget -qO- http://tropometrics-email-api-service:8000/health
```

### Common Issues

**Issue**: Browser shows "NetworkError when attempting to fetch"
- **Cause**: Email API pod is not running or NodePort is blocked
- **Solution**: Check pod status and firewall rules

**Issue**: "Email credentials not configured"
- **Cause**: Kubernetes secret is missing or has wrong keys
- **Solution**: Verify secret with correct keys: `Email-Username`, `Email-Password`, `Email-Server`

**Issue**: SMTP connection timeout
- **Cause**: SMTP server or port is incorrect, or firewall blocking port 587
- **Solution**: Verify `EMAIL_SERVER` format is `host:port` (e.g., `smtp.gmail.com:587`)
