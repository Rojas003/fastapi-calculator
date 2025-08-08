import time
import json
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.activity_service import ActivityService
from app.auth.jwt_handler import decode_jwt

class ActivityTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically track user activities."""
    
    def __init__(self, app):
        super().__init__(app)
        self.tracked_endpoints = {
            "/users/login": ("login", "auth"),
            "/users/register": ("register", "auth"),
            "/users/profile": ("profile_view", "profile"),
            "/users/preferences": ("preferences_update", "preferences"),
            "/calculations": ("calculation", "calculation"),
        }
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Get user info from token
        user_id = self._get_user_id_from_request(request)
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log activity if user is authenticated and endpoint is tracked
        if user_id and self._should_track_endpoint(request.url.path, request.method):
            self._log_activity(
                user_id=user_id,
                request=request,
                response=response,
                duration_ms=duration_ms
            )
        
        return response
    
    def _get_user_id_from_request(self, request: Request) -> int | None:
        """Extract user ID from JWT token in request."""
        try:
            auth_header = request.headers.get("authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            token = auth_header.split(" ")[1]
            payload = decode_jwt(token)
            
            if payload and "user_id" in payload:
                return payload["user_id"]
        except:
            pass
        
        return None
    
    def _should_track_endpoint(self, path: str, method: str) -> bool:
        """Check if this endpoint should be tracked."""
        # Track specific endpoints
        for tracked_path in self.tracked_endpoints:
            if path.startswith(tracked_path):
                return True
        
        # Track calculation operations
        if "/calculations" in path and method in ["POST", "PUT", "DELETE"]:
            return True
        
        return False
    
    def _log_activity(self, user_id: int, request: Request, response: Response, duration_ms: int):
        """Log the activity to database."""
        try:
            db = SessionLocal()
            
            # Determine action and category
            action, category = self._get_action_category(request.url.path, request.method)
            
            # Create description
            description = self._create_description(action, request.method, request.url.path)
            
            # Gather details
            details = {
                "method": request.method,
                "path": str(request.url.path),
                "query_params": dict(request.query_params),
                "status_code": response.status_code
            }
            
            # Determine success status
            success = "success" if response.status_code < 400 else "error"
            
            # Get client info
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")
            
            # Log the activity
            ActivityService.log_activity(
                db=db,
                user_id=user_id,
                action=action,
                category=category,
                description=description,
                details=details,
                ip_address=ip_address,
                user_agent=user_agent,
                endpoint=request.url.path,
                duration_ms=duration_ms,
                success=success
            )
            
            db.close()
            
        except Exception as e:
            # Don't let activity logging break the main request
            print(f"Error logging activity: {e}")
    
    def _get_action_category(self, path: str, method: str) -> tuple[str, str]:
        """Determine action and category from path and method."""
        # Check tracked endpoints first
        for tracked_path, (action, category) in self.tracked_endpoints.items():
            if path.startswith(tracked_path):
                if method == "PUT":
                    return f"{action}_update", category
                elif method == "POST":
                    return action, category
                elif method == "GET":
                    return f"{action}_view", category
        
        # Handle calculations
        if "/calculations" in path:
            if method == "POST":
                return "calculation_create", "calculation"
            elif method == "PUT":
                return "calculation_update", "calculation"
            elif method == "DELETE":
                return "calculation_delete", "calculation"
            elif method == "GET":
                return "calculation_view", "calculation"
        
        # Default
        return "unknown", "unknown"
    
    def _create_description(self, action: str, method: str, path: str) -> str:
        """Create human-readable description."""
        descriptions = {
            "login": "User logged in",
            "register": "User registered account",
            "profile_view": "Viewed profile",
            "profile_update": "Updated profile",
            "preferences_update": "Updated preferences",
            "calculation_create": "Created calculation",
            "calculation_update": "Updated calculation",
            "calculation_delete": "Deleted calculation",
            "calculation_view": "Viewed calculations",
        }
        
        return descriptions.get(action, f"{method} {path}")
