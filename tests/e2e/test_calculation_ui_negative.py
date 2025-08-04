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

    page.goto("http://localhost:8000/login")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_selector("#message")

def test_invalid_operation(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.select_option("#type", "InvalidOp")
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Invalid operation")

def test_division_by_zero(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    page.fill("#a", "10")
    page.fill("#b", "0")
    page.select_option("#type", "Divide")
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Division by zero")

def test_unauthorized_access(page: Page):
    page.goto("http://localhost:8000/calculate")
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.select_option("#type", "Add")
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Unauthorized")

def test_update_nonexistent_calculation(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    page.goto("http://localhost:8000/calculate/update/99999")  # Non-existent ID
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Calculation not found")

def test_delete_nonexistent_calculation(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    page.goto("http://localhost:8000/calculate/delete/99999")  # Non-existent ID
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Calculation not found")
