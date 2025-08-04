import time
from playwright.sync_api import Page, expect

def register_and_login(page: Page):
    page.goto("http://localhost:8000/register")
    timestamp = str(int(time.time() * 1000))
    email = f"user_{timestamp}@example.com"
    password = "securePass123"

    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Registered successfully")

    # Login
    page.goto("http://localhost:8000/login")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Logged in successfully")

def test_calculation_add(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.select_option("#type", "Add")
    page.click("button[type='submit']")
    page.wait_for_selector("#result")
    expect(page.locator("#result")).to_contain_text("15")

def test_update_calculation(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    
    # Create a calculation
    page.fill("#a", "20")
    page.fill("#b", "10")
    page.select_option("#type", "Subtract")
    page.click("button[type='submit']")
    page.wait_for_selector("#result")
    expect(page.locator("#result")).to_contain_text("10")

    # Update the calculation (assumes there's an edit button or endpoint for update)
    page.click("#edit-calculation-1")  # Update this selector if needed
    page.fill("#a", "30")
    page.fill("#b", "5")
    page.select_option("#type", "Divide")
    page.click("button[type='submit']")
    page.wait_for_selector("#result")
    expect(page.locator("#result")).to_contain_text("6")

def test_delete_calculation(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    
    # Create a calculation
    page.fill("#a", "50")
    page.fill("#b", "25")
    page.select_option("#type", "Divide")
    page.click("button[type='submit']")
    page.wait_for_selector("#result")
    expect(page.locator("#result")).to_contain_text("2")

    # Delete the calculation (assumes there's a delete button)
    page.click("#delete-calculation-1")  # Update this selector if needed
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Calculation deleted successfully")
