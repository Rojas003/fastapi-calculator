from playwright.sync_api import Page

def test_register_ui(page: Page):
    page.goto("http://localhost:8000/register")

    email = f"user_{page.evaluate('Date.now()')}@example.com"
    password = "strongpass123"
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")

    # Wait until the #message element appears
    page.wait_for_selector("#message")

    # Wait until the message text updates to include "Registered successfully"
    page.wait_for_function(
        "document.querySelector('#message').innerText.includes('Registered successfully')"
    )

    # Now assert the success message
    assert "Registered successfully" in page.inner_text("#message")
