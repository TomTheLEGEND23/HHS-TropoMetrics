#!/usr/bin/env python3
"""
TropoMetrics API Backend
- Email service (SMTP)
- Weather data API with authentication
Credentials stored as Kubernetes secrets, never exposed to client
"""

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
import httpx
from datetime import datetime

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

# Valid API keys for weather data endpoint
VALID_API_KEYS = [
    "demo",                         # Demo key
]

# Weather data configuration
WEATHER_LOCATION = {
    "latitude": -5.013,
    "longitude": -58.381
}


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
    return {"status": "ok","Backend": "Online"}


@app.get("/api")
async def weather_data_api(request: Request, api_key: Optional[str] = None):
    """
    Weather Data API Endpoint
    Requires API key authentication via query parameter
    Usage: /api?api_key=YOUR_API_KEY
    """
    # Check if api_key is provided
    if not api_key:
        return HTMLResponse(
            content="""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>TropoMetrics Weather API</title>
                <style>
                    body { font-family: 'Monaco', monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }
                    pre { background: #252526; padding: 20px; border-radius: 8px; border: 1px solid #3e3e42; }
                    .error { color: #f48771; }
                </style>
            </head>
            <body>
                <pre class="error">{
  "error": true,
  "status": 401,
  "message": "Missing API key. Use: /api?api_key=YOUR_API_KEY",
  "timestamp": "%s",
  "service": "TropoMetrics Weather API"
}</pre>
            </body>
            </html>
            """ % datetime.utcnow().isoformat() + "Z",
            status_code=401
        )
    
    # Validate API key
    if api_key not in VALID_API_KEYS:
        return HTMLResponse(
            content="""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>TropoMetrics Weather API</title>
                <style>
                    body { font-family: 'Monaco', monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }
                    pre { background: #252526; padding: 20px; border-radius: 8px; border: 1px solid #3e3e42; }
                    .error { color: #f48771; }
                </style>
            </head>
            <body>
                <pre class="error">{
  "error": true,
  "status": 401,
  "message": "Invalid API key",
  "timestamp": "%s",
  "service": "TropoMetrics Weather API"
}</pre>
            </body>
            </html>
            """ % datetime.utcnow().isoformat() + "Z",
            status_code=401
        )
    
    # Fetch weather data from Open-Meteo API
    try:
        async with httpx.AsyncClient() as client:
            api_request = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={WEATHER_LOCATION['latitude']}"
                f"&longitude={WEATHER_LOCATION['longitude']}"
                f"&daily=temperature_2m_max,temperature_2m_min,daylight_duration"
                f"&hourly=precipitation,relative_humidity_2m,soil_moisture_27_to_81cm"
                f"&current=temperature_2m"
                f"&timezone=Europe%2FAmsterdam"
            )
            
            response = await client.get(api_request)
            response.raise_for_status()
            weather_data = response.json()
        
        # Calculate derived values
        now = datetime.utcnow()
        time_hour = now.hour
        if time_hour > 0:
            time_hour -= time_hour % 6
        
        time_line_graph = 24 * 5 + time_hour
        precipitation_5days = []
        amount = 0.0
        
        for i in range(time_hour, min(time_line_graph, len(weather_data['hourly']['precipitation']))):
            amount += weather_data['hourly']['precipitation'][i]
            if (i % 6) == 0 and i != 0:
                precipitation_5days.append({
                    "period_hours": 6,
                    "precipitation_mm": round(amount, 2)
                })
                amount = 0.0
        
        # Calculate irrigation advice
        soil_moisture = weather_data['hourly']['soil_moisture_27_to_81cm'][0]
        irrigation_advice = "Geef water" if soil_moisture <= 0.14 else "Water geven is nu niet nodig"
        
        # Build response
        api_response = {
            "metadata": {
                "service": "TropoMetrics Weather API",
                "version": "1.0.0",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "location": {
                    "latitude": WEATHER_LOCATION['latitude'],
                    "longitude": WEATHER_LOCATION['longitude'],
                    "timezone": "Europe/Amsterdam"
                },
                "source": "Open-Meteo API",
                "endpoint": "/api"
            },
            "current": {
                "temperature_celsius": weather_data['current']['temperature_2m'],
                "temperature_fahrenheit": round(weather_data['current']['temperature_2m'] * 9/5 + 32, 1),
                "timestamp": weather_data['current']['time']
            },
            "daily": {
                "temperature_min_celsius": min(weather_data['daily']['temperature_2m_min']),
                "temperature_max_celsius": max(weather_data['daily']['temperature_2m_max']),
                "daylight_duration_seconds": weather_data['daily']['daylight_duration'][0],
                "daylight_hours": round(weather_data['daily']['daylight_duration'][0] / 3600),
                "daylight_minutes": round((weather_data['daily']['daylight_duration'][0] % 3600) / 60),
                "daylight_formatted": f"{round(weather_data['daily']['daylight_duration'][0] / 3600)}h {round((weather_data['daily']['daylight_duration'][0] % 3600) / 60)}m"
            },
            "moisture": {
                "soil_moisture_27_to_81cm_percentage": round(soil_moisture * 100, 2),
                "soil_moisture_raw": soil_moisture,
                "relative_humidity_percentage": weather_data['hourly']['relative_humidity_2m'][0],
                "timestamp": datetime.utcnow().isoformat() + "Z"
            },
            "irrigation": {
                "advice": irrigation_advice,
                "advice_english": "Give water" if soil_moisture <= 0.14 else "Watering not needed now",
                "needs_water": soil_moisture <= 0.14,
                "threshold": 0.14,
                "current_level": soil_moisture
            },
            "forecast": {
                "precipitation_5day": precipitation_5days,
                "total_precipitation_mm": round(sum(p['precipitation_mm'] for p in precipitation_5days), 2),
                "forecast_periods": len(precipitation_5days)
            },
            "raw_data": {
                "note": "Full hourly and daily data from Open-Meteo API",
                "daily": weather_data['daily'],
                "hourly_sample": {
                    "precipitation_first_24h": weather_data['hourly']['precipitation'][:24],
                    "relative_humidity_first_24h": weather_data['hourly']['relative_humidity_2m'][:24],
                    "soil_moisture_first_24h": weather_data['hourly']['soil_moisture_27_to_81cm'][:24]
                }
            }
        }
        
        # Return as formatted HTML with JSON
        import json
        json_str = json.dumps(api_response, indent=2)
        
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>TropoMetrics Weather API</title>
                <style>
                    body {{ font-family: 'Monaco', monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }}
                    pre {{ background: #252526; padding: 20px; border-radius: 8px; border: 1px solid #3e3e42; overflow-x: auto; }}
                    .header {{ color: #4ec9b0; margin-bottom: 20px; padding: 10px; background: #252526; border-radius: 8px; border-left: 4px solid #4ec9b0; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>🌾 TropoMetrics Weather Data API</h2>
                    <p>Real-time weather data for agricultural sector</p>
                </div>
                <pre>{json_str}</pre>
            </body>
            </html>
            """,
            status_code=200
        )
        
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch weather data: {str(e)}")
        return JSONResponse(
            content={
                "error": True,
                "message": f"Failed to fetch weather data: {str(e)}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "service": "TropoMetrics Weather API"
            },
            status_code=503
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            content={
                "error": True,
                "message": "Internal server error",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "service": "TropoMetrics Weather API"
            },
            status_code=500
        )


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
