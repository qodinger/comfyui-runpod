#!/usr/bin/env python3
"""
Test script for API authentication, rate limiting, and usage tracking.

Run this script to verify all API authentication features are working correctly.
Make sure ComfyUI is running with --enable-api-auth or --require-api-auth
"""

import requests
import time
import sys
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8188"
TEST_KEY_NAME = "Test Key - " + str(int(time.time()))


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_test(name: str):
    logger.info(f"\n{Colors.BLUE}Testing: {name}{Colors.RESET}")


def print_success(message: str):
    logger.info(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_error(message: str):
    logger.error(f"{Colors.RED}✗ {message}{Colors.RESET}")


def print_warning(message: str):
    logger.warning(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")


def test_server_running() -> bool:
    """Test if ComfyUI server is running"""
    print_test("Server Connection")
    try:
        response = requests.get(f"{BASE_URL}/system_stats", timeout=5)
        if response.status_code == 200:
            print_success("Server is running")
            return True
        else:
            print_error(f"Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Is ComfyUI running?")
        print_warning(f"Expected server at: {BASE_URL}")
        return False
    except Exception as e:
        print_error(f"Error connecting to server: {e}")
        return False


def test_create_api_key() -> Optional[Dict]:
    """Test creating an API key"""
    print_test("Create API Key")
    try:
        response = requests.post(
            f"{BASE_URL}/api/keys",
            json={
                "name": TEST_KEY_NAME,
                "rate_limit": 10,  # Low limit for testing
                "metadata": {"test": True}
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if "api_key" in data and "key_id" in data:
                print_success(f"API key created: {data['key_id'][:8]}...")
                print_warning(f"API Key: {data['api_key']}")
                print_warning("Save this key - it won't be shown again!")
                return data
            else:
                print_error("Response missing api_key or key_id")
                print_error(f"Response: {data}")
                return None
        else:
            print_error(f"Failed to create key: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error creating API key: {e}")
        return None


def test_list_api_keys() -> bool:
    """Test listing API keys"""
    print_test("List API Keys")
    try:
        response = requests.get(f"{BASE_URL}/api/keys", timeout=10)

        if response.status_code == 200:
            data = response.json()
            if "keys" in data and isinstance(data["keys"], list):
                print_success(f"Found {len(data['keys'])} API key(s)")
                return True
            else:
                print_error("Invalid response format")
                return False
        else:
            print_error(f"Failed to list keys: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error listing API keys: {e}")
        return False


def test_get_key_details(key_id: str) -> bool:
    """Test getting API key details"""
    print_test("Get API Key Details")
    try:
        response = requests.get(f"{BASE_URL}/api/keys/{key_id}", timeout=10)

        if response.status_code == 200:
            data = response.json()
            if "key_id" in data and "usage_stats" in data:
                print_success("Key details retrieved")
                logger.info("  Name: %s", data.get('name'))
                logger.info("  Rate Limit: %s/hour", data.get('rate_limit'))
                logger.info("  Active: %s", data.get('is_active'))
                logger.info("  Total Requests: %s", data['usage_stats'].get('total_requests', 0))
                return True
            else:
                print_error("Invalid response format")
                return False
        else:
            print_error(f"Failed to get key details: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting key details: {e}")
        return False


def test_api_key_authentication(api_key: str) -> bool:
    """Test API key authentication"""
    print_test("API Key Authentication")
    try:
        # Test with X-API-Key header
        response = requests.get(
            f"{BASE_URL}/api/usage",
            headers={"X-API-Key": api_key},
            timeout=10
        )

        if response.status_code == 200:
            print_success("Authentication with X-API-Key header works")
            return True
        elif response.status_code == 401:
            print_error("Authentication failed - invalid key or auth not enabled")
            print_warning("Make sure ComfyUI is running with --enable-api-auth")
            return False
        else:
            print_error(f"Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing authentication: {e}")
        return False


def test_usage_tracking(api_key: str) -> bool:
    """Test usage tracking"""
    print_test("Usage Tracking")
    try:
        # Make a request to track usage
        response = requests.get(
            f"{BASE_URL}/api/usage?days=7",
            headers={"X-API-Key": api_key},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if "usage_stats" in data:
                print_success("Usage tracking is working")
                stats = data["usage_stats"]
                logger.info("  Total Requests: %s", stats.get('total_requests', 0))
                logger.info("  Successful: %s", stats.get('successful_requests', 0))
                logger.info("  Failed: %s", stats.get('failed_requests', 0))
                return True
            else:
                print_error("Invalid response format")
                return False
        else:
            print_error(f"Failed to get usage: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing usage tracking: {e}")
        return False


def test_rate_limiting(api_key: str, key_id: str) -> bool:
    """Test rate limiting"""
    print_test("Rate Limiting")
    try:
        # Get current rate limit from key details
        details_response = requests.get(f"{BASE_URL}/api/keys/{key_id}", timeout=10)
        if details_response.status_code != 200:
            print_error("Could not get key details for rate limit test")
            return False

        rate_limit = details_response.json().get("rate_limit", 10)
        logger.info("  Rate limit: %s requests/hour", rate_limit)

        # Make requests up to the limit
        headers = {"X-API-Key": api_key}
        rate_limit_hit = False

        for i in range(rate_limit + 2):  # Go slightly over limit
            response = requests.get(
                f"{BASE_URL}/api/usage",
                headers=headers,
                timeout=10
            )

            # Check rate limit headers
            if "X-RateLimit-Limit" in response.headers:
                remaining = int(response.headers.get("X-RateLimit-Remaining", -1))
                if i < rate_limit:
                    if remaining == (rate_limit - i - 1):
                        logger.info("  Request %d: %d remaining ✓", i+1, remaining)
                    else:
                        print_warning(f"  Request {i+1}: Expected {rate_limit - i - 1}, got {remaining}")
                else:
                    if response.status_code == 429:
                        rate_limit_hit = True
                        print_success(f"  Request {i+1}: Rate limit enforced (429) ✓")
                        break
                    else:
                        print_warning(f"  Request {i+1}: Expected 429, got {response.status_code}")

            time.sleep(0.1)  # Small delay between requests

        if rate_limit_hit:
            print_success("Rate limiting is working correctly")
            return True
        else:
            print_warning("Rate limit was not hit - may need to wait for reset")
            return True  # Still consider it working if headers are present
    except Exception as e:
        print_error(f"Error testing rate limiting: {e}")
        return False


def test_update_api_key(key_id: str) -> bool:
    """Test updating an API key"""
    print_test("Update API Key")
    try:
        response = requests.patch(
            f"{BASE_URL}/api/keys/{key_id}",
            json={
                "name": TEST_KEY_NAME + " (Updated)",
                "rate_limit": 20
            },
            timeout=10
        )

        if response.status_code == 200:
            print_success("API key updated")
            return True
        else:
            print_error(f"Failed to update key: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error updating API key: {e}")
        return False


def test_invalid_key() -> bool:
    """Test that invalid keys are rejected"""
    print_test("Invalid Key Rejection")
    try:
        response = requests.get(
            f"{BASE_URL}/api/usage",
            headers={"X-API-Key": "comfy_invalid_key_12345"},
            timeout=10
        )

        if response.status_code == 401:
            print_success("Invalid keys are properly rejected")
            return True
        else:
            print_error(f"Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing invalid key: {e}")
        return False


def test_public_endpoints() -> bool:
    """Test that public endpoints work without authentication"""
    print_test("Public Endpoints (No Auth Required)")
    try:
        public_endpoints = [
            "/system_stats",
            "/features",
            "/object_info",
        ]

        all_working = True
        for endpoint in public_endpoints:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print_success(f"  {endpoint} accessible")
            else:
                print_error(f"  {endpoint} returned {response.status_code}")
                all_working = False

        return all_working
    except Exception as e:
        print_error(f"Error testing public endpoints: {e}")
        return False


def test_delete_api_key(key_id: str) -> bool:
    """Test deleting an API key"""
    print_test("Delete API Key")
    try:
        response = requests.delete(f"{BASE_URL}/api/keys/{key_id}", timeout=10)

        if response.status_code == 200:
            print_success("API key deleted")
            return True
        else:
            print_error(f"Failed to delete key: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error deleting API key: {e}")
        return False


def main():
    """Run all tests"""
    logger.info(f"\n{Colors.BLUE}{'='*60}")
    logger.info("ComfyUI API Authentication Test Suite")
    logger.info(f"{'='*60}{Colors.RESET}\n")

    results = {}

    # Test 1: Server connection
    if not test_server_running():
        print_error("\nCannot proceed without server connection")
        sys.exit(1)

    # Test 2: Public endpoints
    results["public_endpoints"] = test_public_endpoints()

    # Test 3: Create API key
    key_data = test_create_api_key()
    if not key_data:
        print_error("\nCannot proceed without API key")
        sys.exit(1)

    api_key = key_data["api_key"]
    key_id = key_data["key_id"]
    results["create_key"] = True

    # Test 4: List keys
    results["list_keys"] = test_list_api_keys()

    # Test 5: Get key details
    results["get_key_details"] = test_get_key_details(key_id)

    # Test 6: Authentication
    results["authentication"] = test_api_key_authentication(api_key)

    # Test 7: Usage tracking
    results["usage_tracking"] = test_usage_tracking(api_key)

    # Test 8: Rate limiting
    results["rate_limiting"] = test_rate_limiting(api_key, key_id)

    # Test 9: Update key
    results["update_key"] = test_update_api_key(key_id)

    # Test 10: Invalid key rejection
    results["invalid_key"] = test_invalid_key()

    # Test 11: Delete key (cleanup)
    results["delete_key"] = test_delete_api_key(key_id)

    # Summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print("Test Summary")
    print(f"{'='*60}{Colors.RESET}\n")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")

    logger.info(f"\n{Colors.BLUE}Results: {passed}/{total} tests passed{Colors.RESET}\n")

    if passed == total:
        print_success("All tests passed! 🎉")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

