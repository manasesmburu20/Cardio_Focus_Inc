# Testing Guide - CardioFocus Automation

## 3 Ways to Test This Project

### 1. DEMO MODE (Recommended for Quick Demo)
**No browser needed - instant results!**

```bash
python integrated_test.py
```

This runs simulated tests and shows 100% pass rate. Perfect for demonstrating the framework.

---

### 2. INTERACTIVE MODE (Watch Browser Automation!)
**See the automation in action with a real browser!**

**Step 1:** Install Python dependencies
```bash
python -m pip install -r requirements.txt
```

**Step 2:** Run the interactive test
```bash
python interactive_test.py
```

**What happens:**
- Chrome browser opens automatically
- You'll see it navigate to the login page
- Watch it type username and password
- See it click buttons and search for devices
- Browser closes after 5 seconds

**Note:** This uses local HTML files in `mock_portal/` folder - no internet needed!

---

### 3. REAL PORTAL MODE (When You Have Actual Credentials)
**Test against the real CardioFocus portal**

**Step 1:** Edit `.env` file with real credentials
```
PORTAL_URL=https://portal.cardiofocus.com
USERNAME=your_real_username
PASSWORD=your_real_password
API_TOKEN=your_real_token
```

**Step 2:** Edit `integrated_test.py` line 158
```python
demo_mode = False  # Change from True to False
```

**Step 3:** Run the tests
```bash
python integrated_test.py
```

---

## Manual Testing (Open Portal in Browser)

Want to see the mock portal yourself?

1. Navigate to the `mock_portal` folder
2. Double-click `login.html` to open in your browser
3. Enter any username/password (anything works!)
4. Click around and explore the portal

---

## Troubleshooting

**"pip is not recognized"**
- Use: `python -m pip install -r requirements.txt`
- Or: `py -m pip install -r requirements.txt`

**"Python was not found"**
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**"ChromeDriver error"**
- The script auto-downloads ChromeDriver
- Make sure Chrome browser is installed
- Update Chrome to the latest version

**Browser doesn't open**
- Run: `python -m pip install --upgrade selenium webdriver-manager`
- Restart your terminal/PowerShell

---

## What Each Test Does

### API Tests (3 steps):
1. ✓ Authentication - Validates API token
2. ✓ API Request - Retrieves device data
3. ✓ Verification - Checks device status

### UI Tests (7 steps):
1. ✓ Setup - Opens browser
2. ✓ Navigate - Goes to login page
3. ✓ Login - Enters credentials and logs in
4. ✓ Navigation - Clicks "Devices" link
5. ✓ Search - Searches for device by ID
6. ✓ Verification - Checks device status
7. ✓ Teardown - Closes browser

---

## For Recruiters

This project demonstrates:
- ✅ Professional automation framework
- ✅ Both UI (Selenium) and API (requests) testing
- ✅ Proper error handling and reporting
- ✅ Clean, maintainable code structure
- ✅ Security best practices (environment variables)
- ✅ Comprehensive documentation

The demo mode allows you to see the framework working without needing actual portal access.
