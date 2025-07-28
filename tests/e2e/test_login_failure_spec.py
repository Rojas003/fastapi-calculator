# tests/e2e/test_login_failure_playwright.py
import time
from playwright.sync_api import Page, expect

def test_login_failure(page: Page):
    page.goto("http://localhost:8000/login")

    # Attempt to login with invalid credentials
    page.fill("#email", "fake@example.com")
    page.fill("#password", "wrongpassword")
    page.click("button[type='submit']")

    # Wait and assert failure message
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Invalid credentials")
