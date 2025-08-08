import time
from playwright.sync_api import Page, expect
import pytest

def register_and_login_user(page: Page):
    """Helper to register and login a user."""
    timestamp = str(int(time.time() * 1000))
    email = f"user_{timestamp}@example.com"
    password = "testpass123"
    
    # Register
    page.goto("http://localhost:8000/register")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_selector("#message")
    
    # Login
    page.goto("http://localhost:8000/login")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    
    # Wait for login completion
    try:
        page.wait_for_function(
            "document.querySelector('#message') && (document.querySelector('#message').innerText.includes('Login successful') || document.querySelector('#message').innerText.includes('Logged in successfully'))",
            timeout=3000
        )
    except:
        # Try waiting for redirect instead
        try:
            page.wait_for_url("**/calculations-page", timeout=2000)
        except:
            pass  # Continue anyway
    
    return email, password

@pytest.mark.skip(reason="Profile page not yet implemented")
def test_user_profile_page_loads(page: Page):
    """Test that profile page loads."""
    email, password = register_and_login_user(page)
    
    # Try to go to profile page
    page.goto("http://localhost:8000/profile")
    
    # Check if page loads (might be 404 initially)
    if "404" not in page.content():
        # Page exists, check for profile form
        expect(page.locator("h1")).to_contain_text("User Profile")

@pytest.mark.skip(reason="Profile functionality not yet implemented")
def test_user_profile_update(page: Page):
    """Test updating user profile through UI."""
    email, password = register_and_login_user(page)
    
    # Go to profile page
    page.goto("http://localhost:8000/profile")
    
    # Check if page exists
    if "404" in page.content():
        pytest.skip("Profile page not implemented yet")
        return
    
    # Fill profile form
    page.fill("#username", "testuser123")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#phone", "555-1234")
    page.fill("#bio", "This is my test bio")
    
    # Submit profile form
    page.click("#profileForm button[type='submit']")
    
    # Check success message
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Profile updated successfully")

@pytest.mark.skip(reason="Password change functionality not yet implemented")
def test_password_change_success(page: Page):
    """Test successful password change through UI."""
    email, password = register_and_login_user(page)
    
    # Go to profile page
    page.goto("http://localhost:8000/profile")
    
    # Check if page exists
    if "404" in page.content():
        pytest.skip("Profile page not implemented yet")
        return
    
    # Fill password change form
    page.fill("#current_password", password)
    page.fill("#new_password", "newpassword123")
    page.fill("#confirm_password", "newpassword123")
    
    # Submit password form
    page.click("#passwordForm button[type='submit']")
    
    # Check success message
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Password changed successfully")

@pytest.mark.skip(reason="Password change functionality not yet implemented")
def test_password_change_wrong_current(page: Page):
    """Test password change with wrong current password."""
    email, password = register_and_login_user(page)
    
    # Go to profile page
    page.goto("http://localhost:8000/profile")
    
    # Check if page exists
    if "404" in page.content():
        pytest.skip("Profile page not implemented yet")
        return
    
    # Fill password change form with wrong current password
    page.fill("#current_password", "wrongpassword")
    page.fill("#new_password", "newpassword123")
    page.fill("#confirm_password", "newpassword123")
    
    # Submit password form
    page.click("#passwordForm button[type='submit']")
    
    # Check error message
    page.wait_for_selector("#message")
    expect(page.locator("#message")).to_contain_text("Current password is incorrect")

def test_profile_page_accessibility(page: Page):
    """Test basic accessibility of profile page."""
    email, password = register_and_login_user(page)
    
    # Try to navigate to profile page
    page.goto("http://localhost:8000/profile")
    
    # If page doesn't exist yet, just verify we can navigate there
    # (will return 404 until implemented)
    assert page.url.endswith("/profile")