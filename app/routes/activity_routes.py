from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.schemas.activity_log import ActivityLogResponse, ActivityLogFilter, ActivityStatsResponse
from app.services.activity_service import ActivityService
import logging

router = APIRouter()

@router.get("/users/activity", response_model=List[ActivityLogResponse])
def get_user_activity_history(
    category: Optional[str] = Query(None, description="Filter by category"),
    action: Optional[str] = Query(None, description="Filter by action"),
    success: Optional[str] = Query(None, description="Filter by success status"),
    days: int = Query(30, description="Number of days to look back"),
    limit: int = Query(100, description="Maximum number of activities to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's activity history."""
    logging.info(f"Getting activity history for user: {current_user.email}")
    
    activities = ActivityService.get_user_activities(
        db=db,
        user_id=current_user.id,
        category=category,
        action=action,
        success=success,
        days=days,
        limit=limit
    )
    
    return activities

@router.get("/users/activity/stats", response_model=ActivityStatsResponse)
def get_user_activity_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's activity statistics."""
    logging.info(f"Getting activity stats for user: {current_user.email}")
    
    stats = ActivityService.get_activity_stats(db=db, user_id=current_user.id)
    return stats

@router.delete("/users/activity")
def clear_user_activity_history(
    older_than_days: int = Query(90, description="Clear activities older than N days"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clear user's old activity history."""
    logging.info(f"Clearing activity history for user: {current_user.email}")
    
    from datetime import datetime, timedelta
    from app.models.activity_log import ActivityLog
    
    cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)
    
    deleted_count = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id,
        ActivityLog.timestamp < cutoff_date
    ).delete()
    
    db.commit()
    
    logging.info(f"Cleared {deleted_count} old activities for user: {current_user.email}")
    return {"message": f"Cleared {deleted_count} activities older than {older_than_days} days"}
