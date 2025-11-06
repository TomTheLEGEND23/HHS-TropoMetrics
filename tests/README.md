# TropoMetrics Test Suite

Automated testing suite for TropoMetrics web application. Tests both API endpoints and HTML pages across different environments.

## Quick Start

### Linux/macOS One-Liner
```bash
cd /tmp && rm -rf tests && git clone --depth 1 --filter=blob:none --sparse https://github.com/TomTheLEGEND23/HHS-TropoMetrics.git && cd HHS-TropoMetrics && git sparse-checkout set tests && cd tests && python3 run-tests.py
```

### Windows PowerShell One-Liner
```powershell
cd $env:TEMP; if (Test-Path tests) { Remove-Item -Recurse -Force tests }; git clone --depth 1 --filter=blob:none --sparse https://github.com/TomTheLEGEND23/HHS-TropoMetrics.git; cd HHS-TropoMetrics; git sparse-checkout set tests; cd tests; python run-tests.py
```

### Windows Command Prompt One-Liner
```cmd
cd %TEMP% && rmdir /s /q tests 2>nul && git clone --depth 1 --filter=blob:none --sparse https://github.com/TomTheLEGEND23/HHS-TropoMetrics.git && cd HHS-TropoMetrics && git sparse-checkout set tests && cd tests && python run-tests.py
```

## Prerequisites

- Python 3.7 or higher
- Git
- Chrome/Chromium browser
- Required Python packages:
  ```bash
  pip install selenium requests beautifulsoup4
  ```

## Manual Installation

1. Clone the repository (or download the tests folder):
   ```bash
   git clone https://github.com/TomTheLEGEND23/HHS-TropoMetrics.git
   cd HHS-TropoMetrics/tests
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt  # If requirements.txt exists
   # OR manually:
   pip install selenium requests beautifulsoup4
   ```

3. Run the test suite:
   ```bash
   python3 run-tests.py
   ```

## Usage

The test runner will guide you through:

1. **Environment Selection** - Choose target server:
   - Production From TailNet (10.0.0.101:30080)
   - Development From TailNet (10.0.0.101:30081)
   - Production From Lab PC (192.168.20.27:980)
   - Development From Lab PC (192.168.20.27:3981)

2. **Data Source Selection** - Choose data type:
   - Local Data (uses `?api_key=test`)
   - API Data (uses `?api_key=demo`)

3. **Test Selection** - Choose what to test:
   - API Test (`test_API.py`)
   - HTML Test (`test_html.py`)
   - Both tests

## Test Files

### `run-tests.py`
Main test runner script with interactive menu for environment, data source, and test selection.

### `test_API.py`
Tests the API endpoint (`/api?api_key=<key>`). Validates response time and content presence.

### `test_html.py`
Tests the HTML frontend (`/index.html?api_key=<key>`). Validates page load and content rendering.

## Test Output

The script will display:
- Real-time test execution status
- Individual test results (Success/Failure)
- Average response times
- Final summary with pass/fail status

## Environment Variables

The test runner automatically sets these environment variables for the test scripts:
- `TEST_BASE_URL`: Selected target URL
- `TEST_API_KEY`: Selected API key (test/demo)

## Exit Codes

- `0`: All tests passed
- `1`: One or more tests failed
- `130`: User interrupted (Ctrl+C)

## Troubleshooting

### Chrome/ChromeDriver Issues
Ensure Chrome and ChromeDriver are installed and compatible versions:
```bash
# Linux
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver

# Windows
# Download from: https://chromedriver.chromium.org/
```

### Selenium Import Errors
Install Selenium if missing:
```bash
pip install --upgrade selenium
```

### Connection Errors
Verify the target server is accessible:
```bash
curl http://10.0.0.101:30080
```

## Notes

- Tests run in headless Chrome mode (no GUI)
- Each test performs 5 iterations by default
- Tests expect specific text content: "geef water" or "Water geven is nu niet nodig"
- Network access required to reach test environments
