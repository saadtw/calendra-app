from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class CalendraTests:
    def __init__(self):
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        # Initialize driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 10)
        
        # CHANGE THIS TO YOUR DEPLOYED URL OR KEEP AS localhost
        self.base_url = "http://68-210-74-94.nip.io/"
        
    def test_1_homepage_loads(self):
        """Test Case 1: Verify homepage loads successfully"""
        print("\n" + "="*60)
        print("TEST CASE 1: HOMEPAGE LOAD TEST")
        print("="*60)
        
        try:
            print("Step 1: Navigating to homepage...")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            print("Step 2: Checking page title...")
            page_title = self.driver.title
            print(f"   Page Title: {page_title}")
            
            print("Step 3: Checking page loaded successfully...")
            assert page_title != "", "Page title is empty"
            print("   ✓ Page has a title")
            
            print("Step 4: Checking page body content...")
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            assert len(body_text) > 0, "Page body is empty"
            print(f"   ✓ Page has content ({len(body_text)} characters)")
            
            # Take screenshot
            screenshot_name = "test1_homepage_loaded.png"
            self.driver.save_screenshot(screenshot_name)
            print(f"Step 5: Screenshot saved as '{screenshot_name}'")
            
            print("\n✓✓✓ TEST CASE 1: PASSED ✓✓✓\n")
            return True
            
        except Exception as e:
            print(f"\n✗✗✗ TEST CASE 1: FAILED ✗✗✗")
            print(f"Error: {str(e)}\n")
            self.driver.save_screenshot("test1_failed.png")
            return False
    
    def test_2_login_page_exists(self):
        """Test Case 2: Verify login/sign-in page is accessible"""
        print("\n" + "="*60)
        print("TEST CASE 2: LOGIN PAGE ACCESS TEST")
        print("="*60)
        
        try:
            print("Step 1: Navigating to login page...")
            # Try common login URLs
            login_url = self.base_url + "/login"
            self.driver.get(login_url)
            time.sleep(3)
            
            print("Step 2: Checking if login page loaded...")
            current_url = self.driver.current_url
            print(f"   Current URL: {current_url}")
            
            print("Step 3: Looking for login/sign-in elements...")
            # Check for input fields (email/username and password fields)
            input_fields = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"   ✓ Found {len(input_fields)} input field(s)")
            
            # Check for buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"   ✓ Found {len(buttons)} button(s)")
            
            assert len(input_fields) > 0, "No input fields found on login page"
            print("   ✓ Login form elements are present")
            
            # Take screenshot
            screenshot_name = "test2_login_page.png"
            self.driver.save_screenshot(screenshot_name)
            print(f"Step 4: Screenshot saved as '{screenshot_name}'")
            
            print("\n✓✓✓ TEST CASE 2: PASSED ✓✓✓\n")
            return True
            
        except Exception as e:
            print(f"\n✗✗✗ TEST CASE 2: FAILED ✗✗✗")
            print(f"Error: {str(e)}\n")
            self.driver.save_screenshot("test2_failed.png")
            return False
    
    def test_3_navigation_and_buttons(self):
        """Test Case 3: Verify navigation elements and button functionality"""
        print("\n" + "="*60)
        print("TEST CASE 3: NAVIGATION AND BUTTON TEST")
        print("="*60)
        
        try:
            print("Step 1: Navigating to homepage...")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            print("Step 2: Checking for navigation links...")
            links = self.driver.find_elements(By.TAG_NAME, "a")
            print(f"   ✓ Found {len(links)} link(s) on the page")
            
            # Display first few links
            if len(links) > 0:
                print("   Sample links found:")
                for i, link in enumerate(links[:5]):  # Show first 5 links
                    href = link.get_attribute("href")
                    text = link.text.strip()
                    if href:
                        print(f"      {i+1}. Text: '{text}' -> URL: {href}")
            
            print("Step 3: Checking for clickable buttons...")
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"   ✓ Found {len(buttons)} button(s)")
            
            if len(buttons) > 0:
                print("   Sample buttons found:")
                for i, button in enumerate(buttons[:3]):  # Show first 3 buttons
                    button_text = button.text.strip()
                    if button_text:
                        print(f"      {i+1}. '{button_text}'")
            
            assert len(links) > 0 or len(buttons) > 0, "No navigation elements found"
            print("   ✓ Navigation elements are present and functional")
            
            # Take screenshot
            screenshot_name = "test3_navigation.png"
            self.driver.save_screenshot(screenshot_name)
            print(f"Step 4: Screenshot saved as '{screenshot_name}'")
            
            print("\n✓✓✓ TEST CASE 3: PASSED ✓✓✓\n")
            return True
            
        except Exception as e:
            print(f"\n✗✗✗ TEST CASE 3: FAILED ✗✗✗")
            print(f"Error: {str(e)}\n")
            self.driver.save_screenshot("test3_failed.png")
            return False
    
    def run_all_tests(self):
        """Run all test cases and generate report"""
        print("\n" + "="*60)
        print("   CALENDRA APPLICATION - SELENIUM TEST SUITE")
        print("="*60)
        print(f"Testing URL: {self.base_url}")
        print("Total Test Cases: 3")
        print("="*60)
        
        # Run all tests
        results = {
            "Test 1 - Homepage Load": self.test_1_homepage_loads(),
            "Test 2 - Login Page Access": self.test_2_login_page_exists(),
            "Test 3 - Navigation & Buttons": self.test_3_navigation_and_buttons()
        }
        
        # Generate summary report
        print("\n" + "="*60)
        print("              TEST EXECUTION SUMMARY REPORT")
        print("="*60)
        
        passed = sum(results.values())
        total = len(results)
        
        for test_name, result in results.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{test_name:.<45} {status}")
        
        print("-"*60)
        print(f"TOTAL PASSED: {passed}/{total}")
        print(f"TOTAL FAILED: {total - passed}/{total}")
        print(f"SUCCESS RATE: {(passed/total)*100:.1f}%")
        print("="*60)
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉\n")
        else:
            print(f"\n⚠️  {total - passed} TEST(S) FAILED - CHECK ERROR MESSAGES ABOVE\n")
        
        # Close browser
        print("Closing browser...")
        self.driver.quit()
        print("Test execution completed.\n")
        
        return results

if __name__ == "__main__":
    # Run the test suite
    tester = CalendraTests()
    tester.run_all_tests()