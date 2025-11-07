import requests
import time
import os
import sys
import json


# Get base URL and API key from environment variables or use defaults
BASE_URL = os.environ.get("TEST_BASE_URL", "http://10.0.0.101:30081")
API_KEY = os.environ.get("TEST_API_KEY", "demo")

# Build URL with or without API key parameter
if API_KEY:
    TEST_URL = f"{BASE_URL}/api?api_key={API_KEY}"
else:
    TEST_URL = f"{BASE_URL}/api"

# Debug output to show the actual URL being called
print(f"DEBUG: API_KEY value = {API_KEY}")
print(f"DEBUG: API_KEY type = {type(API_KEY)}")
print(f"DEBUG: Full URL = {TEST_URL}")
print()

lijst_zonder_error = []
lijst_met_error = []
lijst_tijden = []
teller = 0 
aantal = 2000

print(f"Testing API endpoint: {TEST_URL}")
print(f"Number of requests: {aantal}")
print("-" * 60)

while teller < aantal:
    teller += 1
    tijd_start = time.time()
    
    try:
        # Make HTTP GET request to the API endpoint
        response = requests.get(TEST_URL, timeout=20)
        tijd_eind = time.time()
        tijd_verschil = tijd_eind - tijd_start
        
        # Check if request was successful (HTTP 200)
        if response.status_code == 200:
            # Try to parse JSON response
            try:
                data = response.json()
                
                # Validate that response contains expected fields
                # Adjust these validations based on your actual API response structure
                if isinstance(data, dict):
                    lijst_zonder_error.append(tijd_verschil)
                    print(f"✓ Request {teller}: Success - {tijd_verschil:.3f}s - Status: {response.status_code}")
                else:
                    lijst_met_error.append(tijd_verschil)
                    print(f"✗ Request {teller}: Invalid JSON structure - {tijd_verschil:.3f}s")
            except json.JSONDecodeError:
                # If response is not JSON, check if it contains expected text
                response_text = response.text.lower()
                if 'geef water' in response_text or 'water geven' in response_text:
                    lijst_zonder_error.append(tijd_verschil)
                    print(f"✓ Request {teller}: Success (HTML response) - {tijd_verschil:.3f}s")
                else:
                    lijst_met_error.append(tijd_verschil)
                    print(f"✗ Request {teller}: Unexpected response format - {tijd_verschil:.3f}s")
        else:
            lijst_met_error.append(tijd_verschil)
            print(f"✗ Request {teller}: HTTP {response.status_code} - {tijd_verschil:.3f}s")
            
    except requests.exceptions.Timeout:
        tijd_eind = time.time()
        tijd_verschil = tijd_eind - tijd_start
        lijst_met_error.append(tijd_verschil)
        print(f"✗ Request {teller}: Timeout after {tijd_verschil:.3f}s")
        
    except requests.exceptions.ConnectionError as e:
        tijd_eind = time.time()
        tijd_verschil = tijd_eind - tijd_start
        lijst_met_error.append(tijd_verschil)
        print(f"✗ Request {teller}: Connection error - {tijd_verschil:.3f}s")
        
    except Exception as e:
        tijd_eind = time.time()
        tijd_verschil = tijd_eind - tijd_start
        lijst_met_error.append(tijd_verschil)
        print(f"✗ Request {teller}: Error - {str(e)[:50]} - {tijd_verschil:.3f}s")

# Print summary
print("\n" + "=" * 60)
print("API Test Summary")
print("=" * 60)
print(f"Total requests: {aantal}")
print(f"Successful: {len(lijst_zonder_error)}")
print(f"Failed: {len(lijst_met_error)}")
print(f"Success rate: {(len(lijst_zonder_error)/aantal)*100:.1f}%")

if lijst_zonder_error:
    average = sum(lijst_zonder_error) / len(lijst_zonder_error)
    min_time = min(lijst_zonder_error)
    max_time = max(lijst_zonder_error)
    print(f"\nLatency Statistics (Successful requests):")
    print(f"  Average: {average:.3f}s")
    print(f"  Min: {min_time:.3f}s")
    print(f"  Max: {max_time:.3f}s")
else:
    print("\nNo successful requests to calculate latency.")

if lijst_met_error:
    print(f"\nFailed requests average time: {sum(lijst_met_error)/len(lijst_met_error):.3f}s")

print("=" * 60)

# Exit with error code if any requests failed
if lijst_met_error:
    sys.exit(1)
else:
    sys.exit(0)
