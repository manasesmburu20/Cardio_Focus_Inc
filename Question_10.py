# - Write a sample Python test that validates the response of a REST API endpoint. 
# The API  returns patient device status in JSON. Write an assertion checking for
# a successful response and  a correct status field.

import requests
import json

def test_patient_device_status():
    """
    Test to validate REST API endpoint returning patient device status
    """
    # API endpoint and authentication
    base_url = "https://api.cardiofocus.com"
    device_id = "DEV-12345"
    endpoint = f"{base_url}/api/devices/{device_id}"
    
    headers = {
        'Authorization': 'Bearer your_api_token_here',
        'Content-Type': 'application/json'
    }
    
    # Make GET request to API
    response = requests.get(endpoint, headers=headers, timeout=10)
    
    # Assertion 1: Check for successful response (HTTP 200)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("✓ Assertion passed: Response status code is 200")
    
    # Parse JSON response
    response_data = response.json()
    
    # Assertion 2: Verify response contains 'status' field
    assert 'status' in response_data, "Response JSON missing 'status' field"
    print("✓ Assertion passed: 'status' field exists in response")
    
    # Assertion 3: Verify status field has correct value
    expected_status = "Active"
    actual_status = response_data['status']
    assert actual_status == expected_status, f"Expected status '{expected_status}', but got '{actual_status}'"
    print(f"✓ Assertion passed: Device status is '{actual_status}'")
    
    # Additional validations (optional but good practice)
    assert 'device_id' in response_data, "Response missing 'device_id' field"
    assert response_data['device_id'] == device_id, "Device ID mismatch"
    print("✓ All assertions passed successfully")
    
    return response_data

# Example with error handling
def test_patient_device_status_with_error_handling():
    """
    Robust version with comprehensive error handling
    """
    try:
        base_url = "https://api.cardiofocus.com"
        device_id = "DEV-12345"
        endpoint = f"{base_url}/api/devices/{device_id}"
        
        headers = {
            'Authorization': 'Bearer your_api_token_here',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        # Assert successful response
        assert response.status_code == 200, \
            f"API request failed with status code {response.status_code}"
        
        # Parse and validate JSON
        response_data = response.json()
        
        # Assert status field exists and is correct
        assert 'status' in response_data, \
            "Response JSON does not contain 'status' field"
        
        expected_status = "Active"
        actual_status = response_data['status']
        
        assert actual_status == expected_status, \
            f"Status validation failed: Expected '{expected_status}', Got '{actual_status}'"
        
        print("✓ Test passed: All assertions successful")
        return True
        
    except requests.exceptions.Timeout:
        print("✗ Test failed: API request timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("✗ Test failed: Connection error")
        return False
    except AssertionError as e:
        print(f"✗ Test failed: {str(e)}")
        return False
    except json.JSONDecodeError:
        print("✗ Test failed: Invalid JSON response")
        return False
    except Exception as e:
        print(f"✗ Test failed: Unexpected error - {str(e)}")
        return False

# Run the test
if __name__ == "__main__":
    print("Running API Test for Patient Device Status\n")
    test_patient_device_status_with_error_handling()


# Expected API Response Format:
"""
{
    "device_id": "DEV-12345",
    "status": "Active",
    "patient_id": "PAT-67890",
    "model": "CardioFocus HeartBeam Pro",
    "last_sync": "2024-03-04T14:30:00Z"
}
"""
