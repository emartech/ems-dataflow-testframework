#!/usr/bin/env python3
"""
Simple test script to verify credential handling.
Run with: python test_credentials.py
"""
import os
from testframework.config.environment import get_credentials

def test_credentials():
    print("Testing credential handling...")

    # Test 1: Without GOOGLE_OAUTH_ACCESS_TOKEN
    if 'GOOGLE_OAUTH_ACCESS_TOKEN' in os.environ:
        del os.environ['GOOGLE_OAUTH_ACCESS_TOKEN']

    creds = get_credentials()
    if creds is None:
        print("✓ Test 1 passed: No token set, returns None (ADC fallback)")
    else:
        print("✗ Test 1 failed: Expected None, got credentials object")
        return False

    # Test 2: With GOOGLE_OAUTH_ACCESS_TOKEN
    test_token = "ya29.test_token_12345"
    os.environ['GOOGLE_OAUTH_ACCESS_TOKEN'] = test_token

    creds = get_credentials()
    if creds is not None and creds.token == test_token:
        print("✓ Test 2 passed: Token set, returns Credentials object with correct token")
    else:
        print("✗ Test 2 failed: Expected Credentials with test token")
        return False

    # Cleanup
    del os.environ['GOOGLE_OAUTH_ACCESS_TOKEN']

    print("\n✓ All tests passed!")
    return True

if __name__ == "__main__":
    test_credentials()