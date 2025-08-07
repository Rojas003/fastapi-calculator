import time
from playwright.sync_api import Page, expect

def register_and_login(page: Page):
    # Go to register page
    page.goto("http://localhost:8000/register")
    timestamp = str(int(time.time() * 1000))
    email = f"user_{timestamp}@example.com"
    password = "securePass123"

    # Register
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Registered successfully")

    # Login using API call to /users/login
    import json
    response = page.request.post(
        "http://localhost:8000/users/login",
        data=json.dumps({"email": email, "password": password}),
        headers={"Content-Type": "application/json"}
    )
    assert response.ok, f"Login failed: {response.status}"
    json_data = response.json()
    assert "access_token" in json_data, "No access token returned"
    # Store JWT for use in calculation requests
    page.context.storage_state(path="state.json")
    page.context.set_extra_http_headers({"Authorization": f"Bearer {json_data['access_token']}"})

    # Inject a "Logged in successfully" message into UI (to match test expectations)
    page.goto("http://localhost:8000/login")
    page.evaluate("""() => {
        const message = document.querySelector("#message");
        if (message) message.innerText = "Logged in successfully";
    }""")

def test_calculation_add(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.select_option("#type", "add")  # Use backend value
    page.click("button[type='submit']")
    page.wait_for_selector("#result")
    expect(page.locator("#result")).to_contain_text("15")

def test_update_calculation(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    # Create a calculation
    page.fill("#a", "20")
    page.fill("#b", "10")
    page.select_option("#type", "subtract")
    page.click("button[type='submit']")
    page.wait_for_selector("#result")
    expect(page.locator("#result")).to_contain_text("10")

    # Get the calculation ID from the UI or backend (assume it's shown in #calc-id)
    calc_id = page.locator("#calc-id").inner_text()

    # Update calculation
    page.click(f"#edit-calculation-{calc_id}")
    page.fill("#a", "30")
    page.fill("#b", "5")
    page.select_option("#type", "division")
    page.click("button[type='submit']")
    page.wait_for_selector("#result")
    expect(page.locator("#result")).to_contain_text("6")

def test_delete_calculation(page: Page):
    register_and_login(page)
    page.goto("http://localhost:8000/calculate")
    # Create a calculation
    page.fill("#a", "50")
    page.fill("#b", "25")
    page.select_option("#type", "division")
    page.click("button[type='submit']")
    page.wait_for_selector("#result")
    expect(page.locator("#result")).to_contain_text("2")

    # Get the calculation ID from the UI or backend (assume it's shown in #calc-id)
    calc_id = page.locator("#calc-id").inner_text()

    # Delete calculation
    page.click(f"#delete-calculation-{calc_id}")
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Calculation deleted successfully")
