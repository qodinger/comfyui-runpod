"""
Rate Limiting Middleware

Implements rate limiting per API key based on hourly request limits.
"""
from aiohttp import web
import logging
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
        
        # Check rate limit
        current_hour_usage = usage_tracker.get_usage_count(api_key.key_id, hours=1)
        
        if current_hour_usage >= api_key.rate_limit:
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
        
        remaining = api_key.rate_limit - current_hour_usage - 1
        reset_time = int(time.time()) + (3600 - (int(time.time()) % 3600))
        
        response.headers['X-RateLimit-Limit'] = str(api_key.rate_limit)
        response.headers['X-RateLimit-Remaining'] = str(max(0, remaining))
        response.headers['X-RateLimit-Reset'] = str(reset_time)
        
        return response
    
    return rate_limit_middleware

