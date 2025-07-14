from app.utils.security import hash_password, verify_password

def test_hash_password_and_verify():
    raw_password = "mysecret123"
    hashed = hash_password(raw_password)

    assert hashed != raw_password
    assert verify_password(raw_password, hashed)

def test_verify_password_fails_with_wrong_password():
    raw_password = "correct"
    wrong_password = "incorrect"
    hashed = hash_password(raw_password)

    assert not verify_password(wrong_password, hashed)
