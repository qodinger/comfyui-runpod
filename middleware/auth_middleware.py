"""
Authentication Middleware for API Key Validation

Validates API keys for protected endpoints.
"""
from aiohttp import web
import logging
from app.api_key_manager import APIKeyManager


# Public endpoints that don't require authentication
PUBLIC_ENDPOINTS = {
    '/',
    '/ws',
    '/system_stats',
    '/features',
    '/object_info',
    '/extensions',
    '/embeddings',
    '/models',
    '/view',
    '/docs',  # API documentation
    '/openapi.json',  # OpenAPI spec
}

# API endpoints that require authentication (when enabled)
API_ENDPOINTS_REQUIRING_AUTH = {
    '/api/prompt',
    '/api/queue',
    '/api/history',
    '/api/interrupt',
    '/api/free',
    '/api/generate',  # Custom endpoint
}


def create_auth_middleware(api_key_manager: APIKeyManager, require_auth: bool = False):
    """
    Create authentication middleware
    
    Args:
        api_key_manager: The API key manager instance
        require_auth: If True, require auth for all /api/* endpoints. 
                     If False, auth is optional but tracked.
    """
    @web.middleware
    async def auth_middleware(request: web.Request, handler):
        path = request.path
        
        # Skip authentication for public endpoints
        if path in PUBLIC_ENDPOINTS or path.startswith('/extensions/') or path.startswith('/docs'):
            return await handler(request)
        
        # Check for API key in header
        api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization')
        
        # Extract key from "Bearer <key>" format
        if api_key and api_key.startswith('Bearer '):
            api_key = api_key[7:]
        
        # For API endpoints, check authentication
        if path.startswith('/api/') or path.startswith('/prompt') or path.startswith('/queue'):
            if require_auth:
                if not api_key:
                    return web.json_response(
                        {"error": "API key required", "error_code": "AUTH_REQUIRED"},
                        status=401
                    )
                
                key_obj = api_key_manager.validate_key(api_key)
                if not key_obj:
                    return web.json_response(
                        {"error": "Invalid API key", "error_code": "INVALID_KEY"},
                        status=401
                    )
                
                # Attach key info to request
                request['api_key'] = key_obj
            else:
                # Optional auth - validate if provided
                if api_key:
                    key_obj = api_key_manager.validate_key(api_key)
                    if key_obj:
                        request['api_key'] = key_obj
        
        return await handler(request)
    
    return auth_middleware

