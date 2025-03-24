import pytest
from myproject import generate_strong_password, save_password, retrieve_password, encrypt_password, decrypt_password, load_key

TEST_SERVICE = "github"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "Secure@123"

def test_generate_password():
    password = generate_strong_password()
    assert isinstance(password, str) 
    assert len(password) >= 12 

def test_encrypt_decrypt():
    key = load_key() 
    encrypted = encrypt_password(TEST_PASSWORD, key)
    decrypted = decrypt_password(encrypted, key)
    assert decrypted == TEST_PASSWORD 

def test_save_and_retrieve_password():
    assert save_password(TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD)
    retrieved_password = retrieve_password(TEST_SERVICE)
    assert retrieved_password == TEST_PASSWORD 
