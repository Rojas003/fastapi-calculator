from playwright.sync_api import Page

def test_register_ui(page: Page):
    page.goto("http://localhost:8000/register")

    username = "user_" + str(page.evaluate("Date.now()"))
    email = f"{username}@example.com"
    password = "strongpass123"

    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")

    page.wait_for_selector("#message")
    assert "Registered successfully" in page.inner_text("#message")
