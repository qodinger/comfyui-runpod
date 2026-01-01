"""
Usage Tracking Middleware

Tracks API usage for analytics and billing.
"""
from aiohttp import web
import time
import logging
from app.usage_tracker import UsageTracker
from app.api_key_manager import APIKey


def create_usage_tracking_middleware(usage_tracker: UsageTracker):
    """
    Create usage tracking middleware
    
    Args:
        usage_tracker: The usage tracker instance
    """
    @web.middleware
    async def usage_tracking_middleware(request: web.Request, handler):
        # Only track API endpoints
        if not (request.path.startswith('/api/') or 
                request.path.startswith('/prompt') or 
                request.path.startswith('/queue')):
            return await handler(request)
        
        # Get API key from request
        api_key: APIKey = request.get('api_key')
        
        if not api_key:
            return await handler(request)
        
        # Track request
        start_time = time.time()
        endpoint = request.path
        
        try:
            response = await handler(request)
            duration = time.time() - start_time
            success = 200 <= response.status < 400
            
            usage_tracker.record_usage(
                key_id=api_key.key_id,
                endpoint=endpoint,
                duration=duration,
                success=success,
                metadata={
                    "method": request.method,
                    "status": response.status
                }
            )
            
            return response
        except Exception as e:
            duration = time.time() - start_time
            usage_tracker.record_usage(
                key_id=api_key.key_id,
                endpoint=endpoint,
                duration=duration,
                success=False,
                metadata={
                    "method": request.method,
                    "error": str(e)
                }
            )
            raise
    
    return usage_tracking_middleware

