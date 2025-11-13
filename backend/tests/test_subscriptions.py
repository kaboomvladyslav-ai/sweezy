from datetime import datetime, timedelta, timezone

from app.models.user import User
from app.services.stripe_service import apply_trial, apply_premium, apply_free
from app.core.database import SessionLocal


def test_trial_and_downgrade_cycle():
    with SessionLocal() as db:
        u = User(email="test@example.com", hashed_password="x")
        db.add(u)
        db.commit()
        db.refresh(u)

        # start trial
        u = apply_trial(db, u, days=7)
        assert u.subscription_status == "trial"
        assert u.subscription_expire_at is not None

        # upgrade to premium
        apply_premium(db, u, subscription_id="sub_123", current_period_end=datetime.now(timezone.utc) + timedelta(days=30))
        db.refresh(u)
        assert u.subscription_status == "premium"
        assert u.stripe_subscription_id == "sub_123"

        # downgrade to free
        apply_free(db, u)
        db.refresh(u)
        assert u.subscription_status == "free"
        assert u.subscription_expire_at is None


