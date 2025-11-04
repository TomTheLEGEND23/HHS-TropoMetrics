#!/usr/bin/env python3
"""
TropoMetrics Email API
Secure backend service for sending emails via SMTP
Credentials stored as Kubernetes secrets, never exposed to client
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TropoMetrics Email API", version="1.0.0")

# CORS configuration - allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Email configuration from environment variables (injected from K8s secrets)
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SERVER = os.getenv("EMAIL_SERVER", "smtp.gmail.com:587")

# Parse server and port
try:
    SMTP_HOST, SMTP_PORT = EMAIL_SERVER.split(":")
    SMTP_PORT = int(SMTP_PORT)
except ValueError:
    SMTP_HOST = EMAIL_SERVER
    SMTP_PORT = 587

# Validate configuration
if not EMAIL_USERNAME or not EMAIL_PASSWORD:
    logger.error("Email credentials not configured! Check Kubernetes secrets.")
else:
    logger.info(f"Email API configured with {EMAIL_USERNAME} via {SMTP_HOST}:{SMTP_PORT}")


class EmailRequest(BaseModel):
    """Email request schema"""
    to: EmailStr
    subject: str
    body: str
    html: bool = False


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "TropoMetrics Email API",
        "status": "healthy",
        "configured": bool(EMAIL_USERNAME and EMAIL_PASSWORD)
    }


@app.get("/health")
async def health():
    """Kubernetes health check"""
    if not EMAIL_USERNAME or not EMAIL_PASSWORD:
        raise HTTPException(status_code=503, detail="Email credentials not configured")
    return {"status": "ok"}


@app.post("/api/send-email")
async def send_email(email: EmailRequest):
    """
    Send an email via SMTP
    
    Request body:
    {
        "to": "recipient@example.com",
        "subject": "Email subject",
        "body": "Email body content",
        "html": false
    }
    """
    
    # Validate credentials
    if not EMAIL_USERNAME or not EMAIL_PASSWORD:
        logger.error("Email credentials not configured")
        raise HTTPException(
            status_code=503,
            detail="Email service not configured. Contact administrator."
        )
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_USERNAME
        msg["To"] = email.to
        msg["Subject"] = email.subject
        
        # Add body
        if email.html:
            msg.attach(MIMEText(email.body, "html"))
        else:
            msg.attach(MIMEText(email.body, "plain"))
        
        # Connect to SMTP server
        logger.info(f"Connecting to {SMTP_HOST}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {email.to}")
        return {
            "status": "success",
            "message": f"Email sent to {email.to}"
        }
    
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed")
        raise HTTPException(
            status_code=401,
            detail="Email authentication failed. Check credentials."
        )
    
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
