# CardioFocus Device Portal - Automation Test Suite
Note: This is a demo, which is why I have included the .env file. In a real project, including the .env file is strictly prohibited for security purposes.

## Overview

This test suite validates core functionality of the CardioFocus portal:
- Secure login authentication
- Device search and retrieval
- Device status verification
- API endpoint validation
- Error handling and reporting

## Requirements

- Python 3.8 or higher
- Chrome browser (latest version)
- Internet connection

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `selenium` - Web browser automation
- `requests` - HTTP API testing
- `python-dotenv` - Environment variable management
- `webdriver-manager` - Automatic ChromeDriver management

### 2. Configure Credentials

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```
PORTAL_URL=https://portal.cardiofocus.com
USERNAME=test_username
PASSWORD=test_password
API_BASE_URL=https://portal.cardiofocus.com/api
API_TOKEN=your_api_token
```

**Important:** The portal login credentials are stored in the `.env` file:
- Username: `test_username` (default)
- Password: `test_password` (default)

These credentials are used to login to the mock web portal interface.

### 3. Email Notifications (Optional)

To enable email notifications, add SMTP settings to `.env`:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@example.com


## Usage

### Run Tests

```bash
python integrated_test.py
```

This runs both UI and API tests, generates a comprehensive report, and automatically updates the web portal.

### Access the Web Portal

To view test results in the web interface:

**Step 1: Open the portal in your browser**

Navigate to the project folder and double-click `mock_portal/login.html`

OR use command line:
```bash
# Windows
start mock_portal\login.html

# macOS
open mock_portal/login.html

# Linux
xdg-open mock_portal/login.html
```

**Step 2: Login with credentials from `.env` file**
- Username: `test_username`
- Password: `test_password`

**Step 3: Navigate to Reports**

Click "Reports" in the navigation menu to view all test execution results. Click any report card to see detailed results.

### View Reports in Portal

After running tests, the reports page is automatically updated. Simply refresh your browser to see the latest test results.

### Run Individual Tests

**API Tests Only:**
```bash
python api_automation.py
```

**UI Tests Only:**
```bash
python ui_automation.py
```

### Customize Test Parameters

Edit the test configuration in `integrated_test.py`:

```python
device_id = "DEV-12345"  # Device to test
expected_status = "Active"  # Expected device status
```

## Project Structure

```
Cardio_Focus_Inc/
├── ui_automation.py       # Selenium-based UI tests
├── api_automation.py      # REST API tests
├── integrated_test.py     # Combined test runner
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── .env                  # Your credentials (not in git)
└── README.md             # This file
```

## Test Reports

Test results are displayed in the console and saved to timestamped files:
- Format: `test_report_YYYYMMDD_HHMMSS.txt`
- Location: Project root directory
- Content: Detailed step-by-step results with pass/fail status

## Design Decisions

### Architecture
- **Modular Design:** Separate scripts for UI and API testing allow independent execution
- **Class-Based Structure:** Encapsulates functionality and maintains state
- **Configuration Management:** Centralized config with environment variables for security

### Error Handling
- Comprehensive try-catch blocks for all operations
- Specific exception handling for common failures (timeout, connection, auth)
- Graceful degradation with informative error messages
- Proper cleanup in finally blocks

### Waits and Timing
- Explicit waits (WebDriverWait) instead of implicit waits
- Configurable timeout (10 seconds default)
- Expected conditions for reliable element detection
- Minimal hard-coded sleeps (only where necessary)

### Security
- Credentials stored in environment variables
- No hardcoded sensitive data
- .env file excluded from version control
- Token-based API authentication

### Reporting
- Clear pass/fail indicators (✓/✗)
- Structured console output
- Persistent file-based reports
- Optional email notifications
- Success rate calculations

## Assumptions

1. **Portal Structure:**
   - Login page has `username`, `password` fields and `login-button` ID
   - Dashboard contains element with class `dashboard`
   - Device page accessible via "Devices" link
   - Device list has ID `device-list`
   - Search box has ID `device-search`
   - Device rows have `data-device-id` attribute
   - Status displayed in `device-status` class

2. **API Structure:**
   - Endpoint: `/api/devices/{device_id}`
   - Authentication: Bearer token
   - Response format: JSON with `status` field
   - Standard HTTP status codes (200, 401, 404)

3. **Environment:**
   - Chrome browser installed
   - Network access to portal and API
   - Valid credentials provided

## Troubleshooting

**ChromeDriver Issues:**
- The script auto-downloads the correct ChromeDriver version
- If issues persist, manually update Chrome browser

**Login Failures:**
- Verify credentials in `.env` file
- Check portal URL is correct
- Ensure account is not locked

**Element Not Found:**
- Portal structure may have changed
- Update selectors in `ui_automation.py`
- Increase wait timeout if needed

**API Errors:**
- Verify API token is valid
- Check API base URL
- Confirm device ID exists

## Future Enhancements

- Parallel test execution
- Screenshot capture on failures
- Integration with CI/CD pipelines
- Support for multiple browsers
- Data-driven testing with CSV/JSON
- Performance metrics collection
