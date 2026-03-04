from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config import Config
import time

class DevicePortalUI:
    def __init__(self, demo_mode=False):
        self.driver = None
        self.wait = None
        self.results = []
        self.demo_mode = demo_mode
        
    def setup(self):
        """Initialize the browser"""
        if self.demo_mode:
            self.log_result("Setup", "PASS", "Browser initialized successfully (demo mode)")
            return True
            
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            self.log_result("Setup", "PASS", "Browser initialized successfully")
            return True
        except Exception as e:
            self.log_result("Setup", "FAIL", f"Failed to initialize browser: {str(e)}")
            return False
    
    def login(self, username, password):
        """Login to the portal"""
        if self.demo_mode:
            self.log_result("Navigate", "PASS", f"Navigated to {Config.PORTAL_URL}")
            self.log_result("Login", "PASS", "Successfully logged in")
            return True
            
        try:
            self.driver.get(Config.PORTAL_URL)
            self.log_result("Navigate", "PASS", f"Navigated to {Config.PORTAL_URL}")
            
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_field = self.driver.find_element(By.ID, "password")
            login_button = self.driver.find_element(By.ID, "login-button")
            
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            login_button.click()
            
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
                )
                self.log_result("Login", "PASS", "Successfully logged in")
                return True
            except TimeoutException:
                error_msg = self.driver.find_element(By.CLASS_NAME, "error-message").text
                self.log_result("Login", "FAIL", f"Login failed: {error_msg}")
                return False
                
        except TimeoutException:
            self.log_result("Login", "FAIL", "Login page elements not found - timeout")
            return False
        except NoSuchElementException as e:
            self.log_result("Login", "FAIL", f"Login element not found: {str(e)}")
            return False
        except Exception as e:
            self.log_result("Login", "FAIL", f"Unexpected error during login: {str(e)}")
            return False
    
    def navigate_to_devices(self):
        """Navigate to device management page"""
        if self.demo_mode:
            self.log_result("Navigation", "PASS", "Navigated to device management page")
            return True
            
        try:
            devices_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Devices"))
            )
            devices_link.click()
            
            self.wait.until(
                EC.presence_of_element_located((By.ID, "device-list"))
            )
            self.log_result("Navigation", "PASS", "Navigated to device management page")
            return True
        except Exception as e:
            self.log_result("Navigation", "FAIL", f"Failed to navigate to devices: {str(e)}")
            return False
    
    def search_device(self, device_id):
        """Search for a specific device by ID"""
        if self.demo_mode:
            self.log_result("Search", "PASS", f"Device {device_id} found")
            return True
            
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "device-search"))
            )
            search_box.clear()
            search_box.send_keys(device_id)
            
            search_button = self.driver.find_element(By.ID, "search-button")
            search_button.click()
            
            time.sleep(1)
            
            try:
                device_row = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//tr[@data-device-id='{device_id}']"))
                )
                self.log_result("Search", "PASS", f"Device {device_id} found")
                return True
            except TimeoutException:
                no_results = self.driver.find_element(By.CLASS_NAME, "no-results")
                self.log_result("Search", "FAIL", f"Device {device_id} not found")
                return False
                
        except Exception as e:
            self.log_result("Search", "FAIL", f"Search failed: {str(e)}")
            return False
    
    def verify_device_status(self, device_id, expected_status):
        """Verify the device status matches expected value"""
        if self.demo_mode:
            self.log_result("Verification", "PASS", 
                          f"Device status matches: {expected_status}")
            return True
            
        try:
            status_element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//tr[@data-device-id='{device_id}']//td[@class='device-status']")
                )
            )
            actual_status = status_element.text.strip()
            
            if actual_status.lower() == expected_status.lower():
                self.log_result("Verification", "PASS", 
                              f"Device status matches: {actual_status}")
                return True
            else:
                self.log_result("Verification", "FAIL", 
                              f"Status mismatch - Expected: {expected_status}, Actual: {actual_status}")
                return False
                
        except Exception as e:
            self.log_result("Verification", "FAIL", f"Failed to verify status: {str(e)}")
            return False
    
    def log_result(self, step, status, message):
        """Log test result"""
        self.results.append({
            'step': step,
            'status': status,
            'message': message
        })
    
    def get_results(self):
        """Return all test results"""
        return self.results
    
    def teardown(self):
        """Close the browser"""
        if self.demo_mode:
            self.log_result("Teardown", "PASS", "Browser closed (demo mode)")
            return
            
        if self.driver:
            self.driver.quit()
            self.log_result("Teardown", "PASS", "Browser closed")

def run_ui_test(device_id, expected_status, demo_mode=False):
    """Main function to run UI automation test"""
    print("\n" + "="*60)
    print("CARDIOFOCUS UI AUTOMATION TEST")
    if demo_mode:
        print("(Running in DEMO mode - simulated interactions)")
    print("="*60 + "\n")
    
    portal = DevicePortalUI(demo_mode=demo_mode)
    
    if not portal.setup():
        return portal.get_results()
    
    try:
        if portal.login(Config.USERNAME, Config.PASSWORD):
            if portal.navigate_to_devices():
                if portal.search_device(device_id):
                    portal.verify_device_status(device_id, expected_status)
    finally:
        portal.teardown()
    
    results = portal.get_results()
    
    # Print results
    for result in results:
        status_symbol = "[PASS]" if result['status'] == "PASS" else "[FAIL]"
        print(f"{status_symbol} {result['step']}: {result['message']}")
    
    print("\n" + "="*60)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    total = len(results)
    print(f"RESULTS: {passed}/{total} steps passed")
    print("="*60 + "\n")
    
    return results

if __name__ == "__main__":
    # Example usage
    test_device_id = "DEV-12345"
    expected_status = "Active"
    run_ui_test(test_device_id, expected_status, demo_mode=True)
