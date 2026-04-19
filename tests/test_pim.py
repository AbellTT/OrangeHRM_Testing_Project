from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from test_auth import login_helper, slow_type

TEST_FIRST_NAME = "mukera"
TEST_LAST_NAME = "123"

# --- TC_005: Add Employee ---
def test_add_employee(driver):
    login_helper(driver, "Admin", "admin123")
    wait = WebDriverWait(driver, 10)
    pim_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "PIM")))
    pim_menu.click()
    add_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add Employee")))
    add_btn.click()
    first_name_input = wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
    last_name_input = driver.find_element(By.NAME, "lastName")
    slow_type(first_name_input, TEST_FIRST_NAME)
    slow_type(last_name_input, TEST_LAST_NAME)
    save_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    save_btn.click()
    toast = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxd-toast-content")))
    assert "Successfully Saved" in toast.text, "Add Employee failed: Success toast not found!"

# --- TC_006: Search Employee ---
def test_search_employee(driver):
    login_helper(driver, "Admin", "admin123")
    wait = WebDriverWait(driver, 10)
    pim_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "PIM")))
    pim_menu.click()
    name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")))
    slow_type(name_input, TEST_FIRST_NAME + " " + TEST_LAST_NAME)
    time.sleep(2) 
    search_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    search_btn.click()
    time.sleep(2)
    table_records = driver.find_elements(By.CLASS_NAME, "oxd-table-card")
    assert len(table_records) >= 1, "Search failed: Employee not found in table!"

# --- TC_007: Delete Employee ---
def test_delete_employee(driver):
    test_search_employee(driver)
    wait = WebDriverWait(driver, 10)
    trash_icon = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "bi-trash")))
    trash_icon.click()
    confirm_delete = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, Delete')]")))
    confirm_delete.click()
    toast = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxd-toast-content")))
    assert "Successfully Deleted" in toast.text, "Delete Employee failed: Success toast not found!"
