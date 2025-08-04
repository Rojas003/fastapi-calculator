import time

def test_login_ui(page):
    # First, register the user via UI
    page.goto("http://localhost:8000/register")

    timestamp = str(int(time.time() * 1000))
    email = f"user_{timestamp}@example.com"
    password = "securePass123"

    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    assert "Registered successfully" in page.inner_text("#message")

    # Then, log in using the same credentials
    page.goto("http://localhost:8000/login")

    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    assert "Logged in successfully" in page.inner_text("#message")
