import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, Dict, Any
from app.models.activity_log import ActivityLog
from app.models.user import User
from app.schemas.activity_log import ActivityLogCreate, ActivityStatsResponse

class ActivityService:
    
    @staticmethod
    def log_activity(
        db: Session,
        user_id: int,
        action: str,
        category: str,
        description: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        endpoint: Optional[str] = None,
        duration_ms: Optional[int] = None,
        success: str = "success"
    ) -> ActivityLog:
        """Log a user activity."""
        
        # Convert details dict to JSON string
        details_json = json.dumps(details) if details else None
        
        activity = ActivityLog(
            user_id=user_id,
            action=action,
            category=category,
            description=description,
            details=details_json,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint=endpoint,
            duration_ms=duration_ms,
            success=success
        )
        
        db.add(activity)
        db.commit()
        db.refresh(activity)
        
        return activity
    
    @staticmethod
    def get_user_activities(
        db: Session,
        user_id: int,
        category: Optional[str] = None,
        action: Optional[str] = None,
        success: Optional[str] = None,
        days: int = 30,
        limit: int = 100
    ) -> list[ActivityLog]:
        """Get user's activity history with filters."""
        
        query = db.query(ActivityLog).filter(ActivityLog.user_id == user_id)
        
        # Apply filters
        if category:
            query = query.filter(ActivityLog.category == category)
        if action:
            query = query.filter(ActivityLog.action == action)
        if success:
            query = query.filter(ActivityLog.success == success)
        
        # Date filter
        if days > 0:
            since_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(ActivityLog.timestamp >= since_date)
        
        # Order and limit
        query = query.order_by(desc(ActivityLog.timestamp)).limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_activity_stats(db: Session, user_id: int) -> ActivityStatsResponse:
        """Get activity statistics for a user."""
        
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Total activities
        total = db.query(ActivityLog).filter(ActivityLog.user_id == user_id).count()
        
        # Activities today
        today_count = db.query(ActivityLog).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.timestamp >= today
        ).count()
        
        # Activities this week
        week_count = db.query(ActivityLog).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.timestamp >= week_ago
        ).count()
        
        # Activities this month
        month_count = db.query(ActivityLog).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.timestamp >= month_ago
        ).count()
        
        # Most common actions
        common_actions = db.query(
            ActivityLog.action,
            ActivityLog.category,
            func.count(ActivityLog.id).label('count')
        ).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.timestamp >= month_ago
        ).group_by(
            ActivityLog.action, ActivityLog.category
        ).order_by(
            desc('count')
        ).limit(5).all()
        
        common_actions_list = [
            {
                "action": action,
                "category": category,
                "count": count
            }
            for action, category, count in common_actions
        ]
        
        # Login frequency (by day of week)
        login_stats = db.query(
            func.extract('dow', ActivityLog.timestamp).label('day_of_week'),
            func.count(ActivityLog.id).label('count')
        ).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.action == 'login',
            ActivityLog.timestamp >= month_ago
        ).group_by('day_of_week').all()
        
        login_frequency = {
            str(int(dow)): count for dow, count in login_stats
        }
        
        # Calculation statistics
        calc_stats = db.query(
            func.count(ActivityLog.id).label('total_calculations')
        ).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.category == 'calculation',
            ActivityLog.timestamp >= month_ago
        ).scalar() or 0
        
        calculation_stats = {
            "total_calculations_month": calc_stats,
            "avg_calculations_per_day": round(calc_stats / 30, 2) if calc_stats > 0 else 0
        }
        
        return ActivityStatsResponse(
            total_activities=total,
            activities_today=today_count,
            activities_this_week=week_count,
            activities_this_month=month_count,
            most_common_actions=common_actions_list,
            login_frequency=login_frequency,
            calculation_stats=calculation_stats
        )