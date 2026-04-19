from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def slow_type(element, text, delay=0.1):
    for character in text:
        element.send_keys(character)
        time.sleep(delay)

def login_helper(driver, username, password):
    driver.get("https://opensource-demo.orangehrmlive.com/")
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = driver.find_element(By.NAME, "password")
    slow_type(username_field, username)
    slow_type(password_field, password)
    driver.find_element(By.TAG_NAME, "button").click()

def logout_helper(driver):
    wait = WebDriverWait(driver, 10)
    profile_icon = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab")))
    profile_icon.click()
    time.sleep(1)
    logout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
    logout_button.click()

# --- TC_001: Valid Login ---
def test_valid_login(driver):
    login_helper(driver, "Admin", "admin123")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("dashboard"))
    assert "dashboard" in driver.current_url, "Login failed: Did not reach dashboard!"

# --- TC_002: Invalid Login ---
def test_invalid_login(driver):
    login_helper(driver, "Admin", "wrongpassword")
    wait = WebDriverWait(driver, 10)
    error_msg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-text.oxd-text--p.oxd-alert-content-text")))
    assert error_msg.text == "Invalid credentials", f"Expected 'Invalid credentials', but got '{error_msg.text}'"

# --- TC_003: Logout ---
def test_logout(driver):
    login_helper(driver, "Admin", "admin123")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("dashboard"))
    logout_helper(driver)
    wait.until(EC.url_contains("login"))
    assert "login" in driver.current_url, "Logout failed: Not on login page!"

# --- TC_004: Session Security ---
def test_session_security_back_button(driver):
    login_helper(driver, "Admin", "admin123")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("dashboard"))
    time.sleep(2)
    logout_helper(driver)
    wait.until(EC.url_contains("login"))
    time.sleep(2)
    driver.back()
    try:
        wait.until(EC.presence_of_element_located((By.NAME, "username")))
    except:
        assert False, "Security flaw: Back button restored the dashboard without redirecting to login!"
