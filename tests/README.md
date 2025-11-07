# TropoMetrics Test Suite

Automated testing suite for TropoMetrics web application. Tests both API endpoints and HTML pages across different environments.

## Quick Start

### Linux/macOS One-Liner
```bash
read -p "Select branch (main/dev): " BRANCH && cd /tmp && rm -rf tropometrics-tests && mkdir -p tropometrics-tests && cd tropometrics-tests && curl -L "https://github.com/TomTheLEGEND23/HHS-TropoMetrics/archive/refs/heads/${BRANCH}.tar.gz" | tar xz --strip=2 "HHS-TropoMetrics-${BRANCH}/tests" && cd tests && pip3 install -q -r requirements.txt && python3 run-tests.py
```

### Windows PowerShell One-Liner
```powershell
$BRANCH = Read-Host "Select branch (main/dev)"; cd $env:TEMP; if (Test-Path tropometrics-tests) { Remove-Item -Recurse -Force tropometrics-tests }; New-Item -ItemType Directory -Path tropometrics-tests | Out-Null; cd tropometrics-tests; Invoke-WebRequest -Uri "https://github.com/TomTheLEGEND23/HHS-TropoMetrics/archive/refs/heads/$BRANCH.zip" -OutFile "repo.zip"; Expand-Archive -Path "repo.zip" -DestinationPath .; cd "HHS-TropoMetrics-$BRANCH/tests"; pip install -q -r requirements.txt; python run-tests.py
```

### Windows Command Prompt One-Liner
```cmd
set /p BRANCH="Select branch (main/dev): " && cd %TEMP% && rmdir /s /q tropometrics-tests 2>nul && mkdir tropometrics-tests && cd tropometrics-tests && curl -L "https://github.com/TomTheLEGEND23/HHS-TropoMetrics/archive/refs/heads/%BRANCH%.zip" -o repo.zip && tar -xf repo.zip && cd HHS-TropoMetrics-%BRANCH%\tests && pip install -q -r requirements.txt && python run-tests.py
```

## Prerequisites

- Python 3.7 or higher (with pip installed)
- curl (Linux/macOS) or PowerShell/CMD with curl support (Windows 10+)
- Chrome/Chromium browser

**Note:** 
- Git is NOT required - one-liners use curl/web download
- Python packages (selenium, requests, beautifulsoup4) are automatically installed by the one-liner

### Installing OpenSSH Client on Windows (if needed)

If you need SSH functionality on Windows, install OpenSSH Client using winget:

```powershell
# Install OpenSSH Client
winget install Microsoft.OpenSSH.Beta

# Verify installation
ssh -V
```

Alternatively, you can install via Windows Settings:
- Settings → Apps → Optional Features → Add a feature → OpenSSH Client

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
   
   **Interactive Mode (default):**
   ```bash
   python3 run-tests.py
   ```
   
   **Direct Mode (with arguments):**
   ```bash
   # Run both tests on dev environment with local data
   python3 run-tests.py --env 2 --api-key test --test both
   
   # Run API test on production with demo API key
   python3 run-tests.py -e 1 -k demo -t api
   
   # Run HTML test with no API key
   python3 run-tests.py --env 3 --api-key none --test html
   
   # Show help and all options
   python3 run-tests.py --help
   ```

## Command-Line Arguments

The test runner supports both **interactive mode** (default) and **direct mode** (with arguments).

### Arguments

- `-e`, `--env <1-4>` - Environment number:
  - `1` - Production From TailNet (10.0.0.101:30080)
  - `2` - Development From TailNet (10.0.0.101:30081)
  - `3` - Production From Lab PC (192.168.20.27:980)
  - `4` - Development From Lab PC (192.168.20.27:981)

- `-k`, `--api-key <test|demo|none>` - API key selection:
  - `test` - Local Data (?api_key=test)
  - `demo` - API Data (?api_key=demo)
  - `none` - No API Key (no parameter)

- `-t`, `--test <api|html|both>` - Which test(s) to run:
  - `api` - API Test only
  - `html` - HTML Test only
  - `both` - Run both tests

**Note:** All three arguments must be provided to use direct mode. If any are missing, the script will fall back to interactive mode.

## Automated Testing with Ansible

Run tests across multiple machines automatically using Ansible.

### Prerequisites for Ansible
- Ansible installed on control machine: `pip install ansible` or `sudo apt install ansible`
- SSH access to Linux/macOS hosts
- WinRM configured on Windows hosts

### Quick Start with Ansible

1. **Edit the inventory file** (`inventory.ini`) to add your test hosts:
   ```ini
   [linux_hosts]
   lab-pc-1 ansible_host=192.168.20.10 ansible_user=user
   
   [windows_hosts]
   lab-pc-2 ansible_host=192.168.20.11 ansible_user=user ansible_connection=winrm
   ```

2. **Run the playbook**:
   ```bash
   # Run with default settings (dev branch, env 2, test api_key, both tests)
   ansible-playbook run-tests.yml
   
   # Run with custom settings
   ansible-playbook run-tests.yml -e "branch=main test_env=1 api_key=demo test_type=both"
   
   # Run on specific host group
   ansible-playbook run-tests.yml --limit windows_hosts
   
   # Run on specific host
   ansible-playbook run-tests.yml --limit lab-pc-1
   ```

### Ansible Variables

Override these with `-e` flag:
- `branch`: Git branch (default: `dev`)
- `test_env`: Environment number 1-4 (default: `2`)
- `api_key`: API key type - test|demo|none (default: `test`)
- `test_type`: Test type - api|html|both (default: `both`)

### Example Ansible Commands

```bash
# Test production environment with demo API on all hosts
ansible-playbook run-tests.yml -e "test_env=1 api_key=demo"

# Test main branch on Windows hosts only
ansible-playbook run-tests.yml -e "branch=main" --limit windows_hosts

# Run HTML test with no API key on specific host
ansible-playbook run-tests.yml -e "api_key=none test_type=html" --limit lab-pc-1

# Dry run to see what will execute
ansible-playbook run-tests.yml --check
```

### Ansible Files

- **`run-tests.yml`** - Main Ansible playbook
- **`inventory.ini`** - Host inventory (edit to add your hosts)
- **`ansible.cfg`** - Ansible configuration
- **`ansible-test.log`** - Log file (created when tests run)

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