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

    # Wait for registration success
    page.wait_for_selector("#message")
    page.wait_for_function(
        "document.querySelector('#message').innerText.includes('Registered successfully')"
    )
    assert "Registered successfully" in page.inner_text("#message")

    # Then, log in with same credentials
    page.goto("http://localhost:8000/login")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")

    # Wait for either login message OR redirect
    try:
        # Check if login message appears first
        page.wait_for_function(
            "document.querySelector('#message').innerText.includes('Login successful')",
            timeout=2000
        )
        assert "Login successful" in page.inner_text("#message")
    except:
        # If message isn't visible quickly enough, verify redirect occurred
        page.wait_for_url("**/calculations-page", timeout=3000)
        assert "/calculations-page" in page.url
