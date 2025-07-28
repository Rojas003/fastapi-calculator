from app.utils.security import get_password_hash, verify_password

def test_password_hashing_and_verification():
    raw_password = "strongpassword123"
    hashed_password = get_password_hash(raw_password)

    # Check that the hash is not the same as the raw password
    assert hashed_password != raw_password

    # Verify that the hashed password is valid
    assert verify_password(raw_password, hashed_password)

    # Negative test: wrong password should not verify
    assert not verify_password("wrongpassword", hashed_password)
