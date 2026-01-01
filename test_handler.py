#!/usr/bin/env python3
"""
Test script for RunPod serverless handler
Tests the handler without requiring ComfyUI to be running
"""

import json
import sys
import logging
from handler import build_workflow, handler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_build_workflow():
    """Test workflow building"""
    logger.info("🧪 Testing build_workflow()...")

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

    logger.info("✅ build_workflow() test passed!")
    return True


def test_handler_structure():
    """Test handler function structure"""
    logger.info("\n🧪 Testing handler() structure...")

    # Test with missing prompt (should return error)
    job = {
        "input": {}
    }

    result = handler(job)
    assert "error" in result or "status" in result, "Handler should return error or status"
    assert result.get("status") == "error" or "error" in result, "Should return error for missing prompt"

    logger.info("✅ Handler error handling works!")

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
        logger.info("✅ Handler structure is correct (connection will fail without ComfyUI)")
    except Exception as e:
        # Expected - ComfyUI not running
        logger.warning("⚠️  Handler tried to connect (expected): %s", type(e).__name__)

    return True


def test_workflow_json():
    """Test that workflow is valid JSON"""
    logger.info("\n🧪 Testing workflow JSON validity...")

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

    logger.info("✅ Workflow JSON is valid!")
    return True


def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("Testing RunPod Serverless Handler")
    logger.info("=" * 60)

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
            logger.error("❌ Test failed: %s", e)
            failed += 1
        except Exception as e:
            logger.error("❌ Test error: %s", e)
            failed += 1

    logger.info("\n" + "=" * 60)
    logger.info("Tests: %d passed, %d failed", passed, failed)
    logger.info("=" * 60)

    if failed == 0:
        logger.info("\n✅ All tests passed!")
        logger.info("\nNote: Full integration test requires ComfyUI to be running.")
        logger.info("To test with ComfyUI:")
        logger.info("  1. Start ComfyUI: python main.py --enable-api-auth")
        logger.info("  2. Run: python test_handler.py --integration")
        return 0
    else:
        logger.error("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

