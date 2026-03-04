import requests
from config import Config

class DevicePortalAPI:
    def __init__(self, demo_mode=False):
        self.base_url = Config.API_BASE_URL
        self.token = Config.API_TOKEN
        self.session = requests.Session()
        self.results = []
        self.demo_mode = demo_mode
        
    def authenticate(self):
        """Set up authentication headers"""
        try:
            if self.demo_mode or self.token:
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                })
                self.log_result("Authentication", "PASS", "API token configured")
                return True
            else:
                self.log_result("Authentication", "FAIL", "No API token provided")
                return False
        except Exception as e:
            self.log_result("Authentication", "FAIL", f"Auth setup failed: {str(e)}")
            return False
    
    def get_device(self, device_id):
        """Retrieve device details from API"""
        if self.demo_mode:
            # Simulate successful API response
            device_data = {
                'device_id': device_id,
                'status': 'Active',
                'model': 'CardioFocus HeartBeam Pro',
                'last_sync': '2024-03-04T14:30:00Z'
            }
            self.log_result("API Request", "PASS", 
                          f"Successfully retrieved device {device_id}")
            return device_data
        
        try:
            url = f"{self.base_url}/devices/{device_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                device_data = response.json()
                self.log_result("API Request", "PASS", 
                              f"Successfully retrieved device {device_id}")
                return device_data
            elif response.status_code == 404:
                self.log_result("API Request", "FAIL", 
                              f"Device {device_id} not found (404)")
                return None
            elif response.status_code == 401:
                self.log_result("API Request", "FAIL", 
                              "Authentication failed (401)")
                return None
            else:
                self.log_result("API Request", "FAIL", 
                              f"API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.log_result("API Request", "FAIL", "Request timeout")
            return None
        except requests.exceptions.ConnectionError:
            self.log_result("API Request", "FAIL", "Connection error")
            return None
        except Exception as e:
            self.log_result("API Request", "FAIL", f"Unexpected error: {str(e)}")
            return None
    
    def verify_status(self, device_data, expected_status):
        """Verify device status field"""
        try:
            if not device_data:
                self.log_result("Verification", "FAIL", "No device data to verify")
                return False
            
            if 'status' not in device_data:
                self.log_result("Verification", "FAIL", "Status field missing in response")
                return False
            
            actual_status = device_data['status']
            
            if actual_status.lower() == expected_status.lower():
                self.log_result("Verification", "PASS", 
                              f"Status matches: {actual_status}")
                return True
            else:
                self.log_result("Verification", "FAIL", 
                              f"Status mismatch - Expected: {expected_status}, Actual: {actual_status}")
                return False
                
        except Exception as e:
            self.log_result("Verification", "FAIL", f"Verification error: {str(e)}")
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

def run_api_test(device_id, expected_status, demo_mode=False):
    """Main function to run API automation test"""
    print("\n" + "="*60)
    print("CARDIOFOCUS API AUTOMATION TEST")
    if demo_mode:
        print("(Running in DEMO mode - simulated responses)")
    print("="*60 + "\n")
    
    api = DevicePortalAPI(demo_mode=demo_mode)
    
    if api.authenticate():
        device_data = api.get_device(device_id)
        api.verify_status(device_data, expected_status)
    
    results = api.get_results()
    
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
    run_api_test(test_device_id, expected_status, demo_mode=True)
