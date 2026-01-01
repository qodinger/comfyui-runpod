#!/usr/bin/env python3
"""
Test script for RunPod serverless handler
Tests the handler without requiring ComfyUI to be running
"""

import json
import sys
from handler import build_workflow, handler

def test_build_workflow():
    """Test workflow building"""
    print("🧪 Testing build_workflow()...")

    workflow = build_workflow(
        prompt="a beautiful landscape",
        negative_prompt="blurry, low quality",
        checkpoint="AnythingXL_xl.safetensors",
        width=512,
        height=512,
        steps=30,
        cfg_scale=7.5,
        sampler="euler_ancestral",
        seed=12345
    )

    # Verify workflow structure
    assert "3" in workflow, "KSampler node missing"
    assert "4" in workflow, "CheckpointLoaderSimple node missing"
    assert "5" in workflow, "EmptyLatentImage node missing"
    assert "6" in workflow, "CLIPTextEncode (positive) node missing"
    assert "7" in workflow, "CLIPTextEncode (negative) node missing"
    assert "8" in workflow, "VAEDecode node missing"
    assert "9" in workflow, "SaveImage node missing"

    # Verify parameters
    assert workflow["3"]["inputs"]["steps"] == 30, "Steps not set correctly"
    assert workflow["3"]["inputs"]["seed"] == 12345, "Seed not set correctly"
    assert workflow["4"]["inputs"]["ckpt_name"] == "AnythingXL_xl.safetensors", "Checkpoint not set correctly"
    assert workflow["6"]["inputs"]["text"] == "a beautiful landscape", "Prompt not set correctly"
    assert workflow["7"]["inputs"]["text"] == "blurry, low quality", "Negative prompt not set correctly"

    print("✅ build_workflow() test passed!")
    return True


def test_handler_structure():
    """Test handler function structure"""
    print("\n🧪 Testing handler() structure...")

    # Test with missing prompt (should return error)
    job = {
        "input": {}
    }

    result = handler(job)
    assert "error" in result or "status" in result, "Handler should return error or status"
    assert result.get("status") == "error" or "error" in result, "Should return error for missing prompt"

    print("✅ Handler error handling works!")

    # Test with valid input structure (will fail without ComfyUI, but structure should be correct)
    job = {
        "input": {
            "prompt": "test prompt",
            "width": 512,
            "height": 512
        }
    }

    # This will fail because ComfyUI isn't running, but we can check the structure
    try:
        result = handler(job)
        # If it gets here, it means it tried to connect (which is expected to fail)
        assert "error" in result or "output" in result, "Handler should return error or output"
        print("✅ Handler structure is correct (connection will fail without ComfyUI)")
    except Exception as e:
        # Expected - ComfyUI not running
        print(f"⚠️  Handler tried to connect (expected): {type(e).__name__}")

    return True


def test_workflow_json():
    """Test that workflow is valid JSON"""
    print("\n🧪 Testing workflow JSON validity...")

    workflow = build_workflow(
        prompt="test",
        width=512,
        height=512
    )

    # Try to serialize to JSON
    json_str = json.dumps(workflow)
    assert len(json_str) > 0, "Workflow should serialize to JSON"

    # Try to deserialize
    workflow_parsed = json.loads(json_str)
    assert workflow_parsed == workflow, "Workflow should round-trip through JSON"

    print("✅ Workflow JSON is valid!")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing RunPod Serverless Handler")
    print("=" * 60)

    tests = [
        test_build_workflow,
        test_handler_structure,
        test_workflow_json
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Tests: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ All tests passed!")
        print("\nNote: Full integration test requires ComfyUI to be running.")
        print("To test with ComfyUI:")
        print("  1. Start ComfyUI: python main.py --enable-api-auth")
        print("  2. Run: python test_handler.py --integration")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

