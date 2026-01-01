"""
Rate Limiting Middleware

Implements rate limiting per API key based on hourly request limits.
"""
from aiohttp import web
import time
from app.usage_tracker import UsageTracker
from app.api_key_manager import APIKey


def create_rate_limit_middleware(usage_tracker: UsageTracker):
    """
    Create rate limiting middleware

    Args:
        usage_tracker: The usage tracker instance
    """
    @web.middleware
    async def rate_limit_middleware(request: web.Request, handler):
        # Only apply rate limiting to API endpoints
        if not (request.path.startswith('/api/') or
                request.path.startswith('/prompt') or
                request.path.startswith('/queue')):
            return await handler(request)

        # Get API key from request (set by auth middleware)
        api_key: APIKey = request.get('api_key')

        if not api_key:
            # No rate limiting for unauthenticated requests (if allowed)
            return await handler(request)

        # Fixed Bug 1: Increment usage count BEFORE checking to prevent TOCTOU race condition
        # This ensures concurrent requests see the updated count immediately
        # Use >= instead of > to correctly reject when limit is exactly reached
        new_count = usage_tracker.increment_usage_count(api_key.key_id)

        if new_count >= api_key.rate_limit:
            # Over limit - decrement the count we just incremented
            current_hour = int(time.time() // 3600)
            usage_tracker.hourly_counts[api_key.key_id][current_hour] = max(0, usage_tracker.hourly_counts[api_key.key_id][current_hour] - 1)
            return web.json_response(
                {
                    "error": "Rate limit exceeded",
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "limit": api_key.rate_limit,
                    "reset_in": 3600 - (int(time.time()) % 3600)
                },
                status=429,
                headers={
                    "X-RateLimit-Limit": str(api_key.rate_limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + (3600 - (int(time.time()) % 3600)))
                }
            )

        # Add rate limit headers
        response = await handler(request)

        # Calculate remaining: limit - new_count
        # new_count already includes the increment for this request, so the calculation is correct
        remaining = api_key.rate_limit - new_count
        reset_time = int(time.time()) + (3600 - (int(time.time()) % 3600))

        response.headers['X-RateLimit-Limit'] = str(api_key.rate_limit)
        response.headers['X-RateLimit-Remaining'] = str(max(0, remaining))
        response.headers['X-RateLimit-Reset'] = str(reset_time)

        return response

    return rate_limit_middleware
