import pytest
from app.schemas.user import UserPreferences, UserPreferencesUpdate

def test_user_preferences_schema():
    """Test UserPreferences schema with all fields."""
    prefs = UserPreferences(
        theme="dark",
        language="es", 
        timezone="America/New_York",
        notifications_enabled=False,
        email_notifications=True,
        calculation_history_limit=250,
        auto_save_calculations=False
    )
    
    assert prefs.theme == "dark"
    assert prefs.language == "es"
    assert prefs.timezone == "America/New_York"
    assert prefs.notifications_enabled == False
    assert prefs.email_notifications == True
    assert prefs.calculation_history_limit == 250
    assert prefs.auto_save_calculations == False

def test_user_preferences_defaults():
    """Test UserPreferences schema with default values."""
    prefs = UserPreferences()
    
    assert prefs.theme == "light"
    assert prefs.language == "en"
    assert prefs.timezone == "UTC"
    assert prefs.notifications_enabled == True
    assert prefs.email_notifications == True
    assert prefs.calculation_history_limit == 100
    assert prefs.auto_save_calculations == True

def test_user_preferences_update_partial():
    """Test UserPreferencesUpdate schema with partial data."""
    update = UserPreferencesUpdate(
        theme="dark",
        notifications_enabled=False
    )
    
    assert update.theme == "dark"
    assert update.notifications_enabled == False
    assert update.language is None  # Not provided
    assert update.timezone is None  # Not provided

def test_theme_validation():
    """Test theme field validation."""
    # Valid themes
    valid_themes = ["light", "dark", "auto"]
    for theme in valid_themes:
        prefs = UserPreferences(theme=theme)
        assert prefs.theme == theme

def test_language_validation():
    """Test language field validation.""" 
    # Valid languages
    valid_languages = ["en", "es", "fr"]
    for lang in valid_languages:
        prefs = UserPreferences(language=lang)
        assert prefs.language == lang