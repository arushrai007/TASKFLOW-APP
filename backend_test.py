import requests
import sys
import json
from datetime import datetime

class TODOAPITester:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
        
        result = {
            "test": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}: {details}")

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=test_headers)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if not success:
                details += f" (Expected: {expected_status})"
                try:
                    error_data = response.json()
                    details += f" - {error_data.get('detail', 'No error details')}"
                except:
                    details += f" - Response: {response.text[:100]}"
            
            self.log_test(name, success, details)
            
            if success:
                try:
                    return response.json()
                except:
                    return {"message": "Success"}
            return None

        except Exception as e:
            self.log_test(name, False, f"Exception: {str(e)}")
            return None

    def test_health_check(self):
        """Test API health check"""
        return self.run_test("Health Check", "GET", "", 200)

    def test_signup(self, name, email, password):
        """Test user signup"""
        data = {"name": name, "email": email, "password": password}
        response = self.run_test("User Signup", "POST", "auth/signup", 201, data)
        
        if response and 'access_token' in response:
            self.token = response['access_token']
            self.user_id = response['user']['id']
            return True
        return False

    def test_signin(self, email, password):
        """Test user signin"""
        data = {"email": email, "password": password}
        response = self.run_test("User Signin", "POST", "auth/signin", 200, data)
        
        if response and 'access_token' in response:
            self.token = response['access_token']
            self.user_id = response['user']['id']
            return True
        return False

    def test_duplicate_signup(self, name, email, password):
        """Test duplicate email signup (should fail)"""
        data = {"name": name, "email": email, "password": password}
        self.run_test("Duplicate Email Signup", "POST", "auth/signup", 400, data)

    def test_invalid_signin(self, email, password):
        """Test invalid credentials signin (should fail)"""
        data = {"email": email, "password": password}
        self.run_test("Invalid Credentials Signin", "POST", "auth/signin", 401, data)

    def test_logout(self):
        """Test user logout"""
        return self.run_test("User Logout", "POST", "auth/logout", 200)

    def test_create_task(self, title, description=None, priority="Medium"):
        """Test task creation"""
        data = {"title": title, "priority": priority}
        if description:
            data["description"] = description
        
        response = self.run_test("Create Task", "POST", "tasks", 201, data)
        return response.get('id') if response else None

    def test_get_tasks(self):
        """Test getting all tasks"""
        response = self.run_test("Get All Tasks", "GET", "tasks", 200)
        return response if response else []

    def test_get_tasks_filtered(self, completed=None):
        """Test getting filtered tasks"""
        endpoint = "tasks"
        if completed is not None:
            endpoint += f"?completed={str(completed).lower()}"
        
        filter_name = "All" if completed is None else ("Completed" if completed else "Incomplete")
        response = self.run_test(f"Get {filter_name} Tasks", "GET", endpoint, 200)
        return response if response else []

    def test_get_tasks_sorted(self, sort_by="created_at", sort_order=-1):
        """Test getting sorted tasks"""
        endpoint = f"tasks?sort_by={sort_by}&sort_order={sort_order}"
        sort_name = "Priority" if sort_by == "priority" else "Date"
        order_name = "Desc" if sort_order == -1 else "Asc"
        
        response = self.run_test(f"Get Tasks Sorted by {sort_name} ({order_name})", "GET", endpoint, 200)
        return response if response else []

    def test_update_task(self, task_id, title=None, description=None, priority=None):
        """Test task update"""
        data = {}
        if title:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if priority:
            data["priority"] = priority
        
        return self.run_test("Update Task", "PUT", f"tasks/{task_id}", 200, data)

    def test_mark_complete(self, task_id, completed=True):
        """Test marking task as complete/incomplete"""
        endpoint = f"tasks/{task_id}/complete?completed={str(completed).lower()}"
        action = "Complete" if completed else "Incomplete"
        return self.run_test(f"Mark Task {action}", "PATCH", endpoint, 200)

    def test_delete_task(self, task_id):
        """Test task deletion"""
        return self.run_test("Delete Task", "DELETE", f"tasks/{task_id}", 200)

    def test_unauthorized_access(self):
        """Test accessing protected endpoints without token"""
        old_token = self.token
        self.token = None
        self.run_test("Unauthorized Task Access", "GET", "tasks", 401)
        self.token = old_token

    def test_invalid_token_access(self):
        """Test accessing protected endpoints with invalid token"""
        old_token = self.token
        self.token = "invalid_token"
        self.run_test("Invalid Token Access", "GET", "tasks", 401)
        self.token = old_token

    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*50}")
        print(f"TEST SUMMARY")
        print(f"{'='*50}")
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Print failed tests
        failed_tests = [test for test in self.test_results if not test['success']]
        if failed_tests:
            print(f"\nFAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['details']}")

def main():
    print("🚀 Starting TODO API Tests...")
    tester = TODOAPITester()
    
    # Test unique user data
    timestamp = datetime.now().strftime('%H%M%S')
    test_email = f"test_user_{timestamp}@example.com"
    test_name = f"Test User {timestamp}"
    test_password = "TestPass123!"
    
    # 1. Health Check
    tester.test_health_check()
    
    # 2. Authentication Tests
    print("\n📝 Testing Authentication...")
    
    # Test signup
    if not tester.test_signup(test_name, test_email, test_password):
        print("❌ Signup failed, stopping tests")
        return 1
    
    # Test duplicate signup
    tester.test_duplicate_signup(test_name, test_email, test_password)
    
    # Test invalid signin
    tester.test_invalid_signin(test_email, "wrong_password")
    
    # Test valid signin (with new credentials)
    tester.token = None  # Clear token to test signin
    if not tester.test_signin(test_email, test_password):
        print("❌ Signin failed, stopping tests")
        return 1
    
    # 3. Authorization Tests
    print("\n🔒 Testing Authorization...")
    tester.test_unauthorized_access()
    tester.test_invalid_token_access()
    
    # 4. Task Management Tests
    print("\n📋 Testing Task Management...")
    
    # Create tasks with different priorities
    task1_id = tester.test_create_task("High Priority Task", "This is urgent", "High")
    task2_id = tester.test_create_task("Medium Priority Task", "This is normal", "Medium")
    task3_id = tester.test_create_task("Low Priority Task", "This can wait", "Low")
    task4_id = tester.test_create_task("Task without description", None, "Medium")
    
    if not task1_id:
        print("❌ Task creation failed, stopping task tests")
        tester.print_summary()
        return 1
    
    # Test getting all tasks
    all_tasks = tester.test_get_tasks()
    
    # Test filtering
    print("\n🔍 Testing Filtering...")
    tester.test_get_tasks_filtered(completed=False)  # Incomplete tasks
    tester.test_get_tasks_filtered(completed=True)   # Completed tasks
    tester.test_get_tasks_filtered(completed=None)   # All tasks
    
    # Test sorting
    print("\n📊 Testing Sorting...")
    tester.test_get_tasks_sorted("priority", -1)     # Priority desc (High->Low)
    tester.test_get_tasks_sorted("priority", 1)      # Priority asc (Low->High)
    tester.test_get_tasks_sorted("created_at", -1)   # Date desc (newest first)
    tester.test_get_tasks_sorted("created_at", 1)    # Date asc (oldest first)
    
    # Test task updates
    print("\n✏️ Testing Task Updates...")
    tester.test_update_task(task1_id, title="Updated High Priority Task")
    tester.test_update_task(task2_id, description="Updated description")
    tester.test_update_task(task3_id, priority="High")
    
    # Test completion toggle
    print("\n✅ Testing Task Completion...")
    tester.test_mark_complete(task1_id, True)   # Mark complete
    tester.test_mark_complete(task1_id, False)  # Mark incomplete
    
    # Test task deletion
    print("\n🗑️ Testing Task Deletion...")
    tester.test_delete_task(task4_id)
    
    # Test logout
    print("\n👋 Testing Logout...")
    tester.test_logout()
    
    # Print final summary
    tester.print_summary()
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())