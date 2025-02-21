from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from app.db import get_db
from app.models import UserSession


def cleanup_inactive_sessions():
    db = next(get_db())
    try:
        cutoff = datetime.utcnow() - timedelta(days=30)
        db.query(UserSession).filter(UserSession.last_activity < cutoff).delete()
        db.commit()
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_inactive_sessions, "interval", hours=24)
scheduler.start()
