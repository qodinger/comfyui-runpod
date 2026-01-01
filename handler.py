"""
RunPod Serverless Handler for ComfyUI
This handler wraps ComfyUI API for RunPod serverless deployment.
"""

import os
import time
import uuid
import logging
import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin

import runpod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ComfyUI server URL (defaults to localhost for serverless)
COMFYUI_URL = os.getenv("COMFYUI_URL", "http://localhost:8188")
COMFYUI_API_KEY = os.getenv("COMFYUI_API_KEY", None)  # Optional API key for authentication

# Timeout settings
GENERATION_TIMEOUT = int(os.getenv("GENERATION_TIMEOUT", "300"))  # 5 minutes default
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "1.0"))  # 1 second


def build_workflow(
    prompt: str,
    negative_prompt: str = "",
    checkpoint: str = "AnythingXL_xl.safetensors",
    width: int = 512,
    height: int = 512,
    steps: int = 30,
    cfg_scale: float = 7.5,
    sampler: str = "euler_ancestral",
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Build a ComfyUI workflow JSON from parameters.

    Args:
        prompt: Positive prompt text
        negative_prompt: Negative prompt text
        checkpoint: Model checkpoint name
        width: Image width
        height: Image height
        steps: Number of sampling steps
        cfg_scale: CFG scale
        sampler: Sampler name
        seed: Random seed (None for random)

    Returns:
        ComfyUI workflow dictionary
    """
    if seed is None:
        seed = int(time.time() * 1000) % (2**31)

    workflow = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "cfg": cfg_scale,
                "denoise": 1.0,
                "latent_image": ["5", 0],
                "model": ["4", 0],
                "negative": ["7", 0],
                "positive": ["6", 0],
                "sampler_name": sampler,
                "scheduler": "normal",
                "seed": seed,
                "steps": steps
            }
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": checkpoint
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "batch_size": 1,
                "height": height,
                "width": width
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["4", 1],
                "text": prompt
            }
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["4", 1],
                "text": negative_prompt or "bad hands, blurry, low quality, distorted"
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            }
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": ["8", 0]
            }
        }
    }

    return workflow


def queue_prompt(workflow: Dict[str, Any], client_id: Optional[str] = None) -> str:
    """
    Queue a prompt in ComfyUI and return the prompt_id.

    Args:
        workflow: ComfyUI workflow dictionary
        client_id: Optional client ID

    Returns:
        prompt_id string
    """
    prompt_id = str(uuid.uuid4())

    payload = {
        "prompt": workflow,
        "prompt_id": prompt_id
    }

    if client_id:
        payload["client_id"] = client_id

    url = urljoin(COMFYUI_URL, "/prompt")
    headers = {"Content-Type": "application/json"}

    if COMFYUI_API_KEY:
        headers["X-API-Key"] = COMFYUI_API_KEY

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    result = response.json()
    if "error" in result:
        raise Exception(f"ComfyUI error: {result['error']}")

    return prompt_id


def get_image(prompt_id: str) -> Optional[str]:
    """
    Get the generated image URL from ComfyUI history.

    Args:
        prompt_id: The prompt ID to check

    Returns:
        Image URL or None if not ready
    """
    url = urljoin(COMFYUI_URL, f"/history/{prompt_id}")
    headers = {}

    if COMFYUI_API_KEY:
        headers["X-API-Key"] = COMFYUI_API_KEY

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    history = response.json()

    if prompt_id in history:
        images = history[prompt_id]
        if images and len(images) > 0:
            # Get the first output image
            output = images[0]
            if "outputs" in output and "9" in output["outputs"]:
                images_data = output["outputs"]["9"]["images"]
                if images_data and len(images_data) > 0:
                    filename = images_data[0]["filename"]
                    subfolder = images_data[0].get("subfolder", "")
                    image_url = urljoin(COMFYUI_URL, f"/view?filename={filename}&subfolder={subfolder}&type=output")
                    return image_url

    return None


def wait_for_image(prompt_id: str, timeout: int = GENERATION_TIMEOUT) -> Optional[str]:
    """
    Wait for image generation to complete.

    Args:
        prompt_id: The prompt ID to wait for
        timeout: Maximum time to wait in seconds

    Returns:
        Image URL or None if timeout
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        image_url = get_image(prompt_id)
        if image_url:
            return image_url

        time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"Image generation timed out after {timeout} seconds")


def handler(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    RunPod serverless handler for ComfyUI image generation.

    Expected input format:
    {
        "input": {
            "prompt": "your prompt text",
            "negative_prompt": "optional negative prompt",
            "checkpoint": "model name (optional)",
            "width": 512,
            "height": 512,
            "steps": 30,
            "cfg_scale": 7.5,
            "sampler": "euler_ancestral",
            "seed": 12345 (optional)
        }
    }

    Returns:
    {
        "output": {
            "image_url": "http://...",
            "prompt_id": "...",
            "status": "success"
        }
    }
    """
    try:
        input_data = job.get("input", {})

        # Extract parameters
        prompt = input_data.get("prompt")
        if not prompt:
            return {
                "error": "Missing required parameter: prompt",
                "status": "error"
            }

        negative_prompt = input_data.get("negative_prompt", "")
        checkpoint = input_data.get("checkpoint", "AnythingXL_xl.safetensors")
        width = int(input_data.get("width", 512))
        height = int(input_data.get("height", 512))
        steps = int(input_data.get("steps", 30))
        cfg_scale = float(input_data.get("cfg_scale", 7.5))
        sampler = input_data.get("sampler", "euler_ancestral")
        seed = input_data.get("seed")

        logger.info(f"Generating image with prompt: {prompt[:50]}...")

        # Build workflow
        workflow = build_workflow(
            prompt=prompt,
            negative_prompt=negative_prompt,
            checkpoint=checkpoint,
            width=width,
            height=height,
            steps=steps,
            cfg_scale=cfg_scale,
            sampler=sampler,
            seed=seed
        )

        # Queue prompt
        prompt_id = queue_prompt(workflow)
        logger.info(f"Queued prompt: {prompt_id}")

        # Wait for image
        image_url = wait_for_image(prompt_id, timeout=GENERATION_TIMEOUT)

        if not image_url:
            return {
                "error": "Image generation failed or timed out",
                "prompt_id": prompt_id,
                "status": "error"
            }

        logger.info(f"Image generated: {image_url}")

        return {
            "output": {
                "image_url": image_url,
                "prompt_id": prompt_id,
                "status": "success",
                "prompt": prompt,
                "parameters": {
                    "width": width,
                    "height": height,
                    "steps": steps,
                    "cfg_scale": cfg_scale,
                    "sampler": sampler,
                    "seed": seed,
                    "checkpoint": checkpoint
                }
            }
        }

    except TimeoutError as e:
        logger.error(f"Timeout: {e}")
        return {
            "error": str(e),
            "status": "timeout"
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return {
            "error": f"ComfyUI connection error: {str(e)}",
            "status": "error"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }


# Register handler with RunPod
if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})

