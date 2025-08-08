from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import json

class ActivityLogCreate(BaseModel):
    action: str
    category: str
    description: Optional[str] = None
    details: Optional[dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    endpoint: Optional[str] = None
    duration_ms: Optional[int] = None
    success: str = "success"

class ActivityLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    category: str
    description: Optional[str] = None
    details: Optional[str] = None  # JSON string
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    endpoint: Optional[str] = None
    timestamp: datetime
    duration_ms: Optional[int] = None
    success: str
    
    class Config:
        from_attributes = True
    
    @property
    def details_dict(self) -> dict:
        """Parse details JSON string to dict."""
        if self.details:
            try:
                return json.loads(self.details)
            except:
                return {}
        return {}

class ActivityLogFilter(BaseModel):
    category: Optional[str] = None
    action: Optional[str] = None
    success: Optional[str] = None
    days: Optional[int] = 30  # Last N days
    limit: Optional[int] = 100

class ActivityStatsResponse(BaseModel):
    total_activities: int
    activities_today: int
    activities_this_week: int
    activities_this_month: int
    most_common_actions: List[dict]
    login_frequency: dict
    calculation_stats: dict
