from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.news import News
from ..utils.ids import generate_uuid


class NewsService:
  @staticmethod
  def list_news(db: Session, language: Optional[str] = None, limit: int = 50) -> List[News]:
    query = db.query(News).order_by(News.published_at.desc())
    if language:
      query = query.filter(News.language == language)
    return query.limit(limit).all()

  @staticmethod
  def get(db: Session, news_id: str) -> Optional[News]:
    return db.query(News).filter(News.id == news_id).first()

  @staticmethod
  def create(db: Session, **data) -> News:
    news = News(
      id=generate_uuid(),
      title=data["title"],
      summary=data.get("summary", ""),
      url=str(data["url"]),
      source=data.get("source", "Sweezy"),
      language=data.get("language", "uk"),
      published_at=data.get("published_at") or datetime.utcnow(),
      image_url=str(data["image_url"]) if data.get("image_url") else None,
      created_at=datetime.utcnow(),
      updated_at=datetime.utcnow(),
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return news

  @staticmethod
  def update(db: Session, news: News, **data) -> News:
    for field, value in data.items():
      if value is not None:
        setattr(news, field, value)
    news.updated_at = datetime.utcnow()
    db.add(news)
    db.commit()
    db.refresh(news)
    return news

  @staticmethod
  def delete(db: Session, news: News) -> None:
    db.delete(news)
    db.commit()
from __future__ import annotations
\nfrom datetime import datetime\nfrom typing import List, Optional\n\nfrom sqlalchemy.orm import Session\nfrom ..models.news import News\nfrom ..utils.ids import generate_uuid\n\n\nclass NewsService:\n    @staticmethod\n    def list_news(db: Session, language: Optional[str] = None, limit: int = 50) -> List[News]:\n        q = db.query(News).order_by(News.published_at.desc())\n        if language:\n            q = q.filter(News.language == language)\n        return q.limit(limit).all()\n\n    @staticmethod\n    def get(db: Session, news_id: str) -> Optional[News]:\n        return db.query(News).filter(News.id == news_id).first()\n\n    @staticmethod\n    def create(db: Session, **data) -> News:\n        news = News(\n            id=generate_uuid(),\n            title=data[\"title\"],\n            summary=data.get(\"summary\", \"\"),\n            url=str(data[\"url\"]),\n            source=data.get(\"source\", \"Sweezy\"),\n            language=data.get(\"language\", \"uk\"),\n            published_at=data.get(\"published_at\", datetime.utcnow()),\n            image_url=str(data[\"image_url\"]) if data.get(\"image_url\") else None,\n            created_at=datetime.utcnow(),\n            updated_at=datetime.utcnow(),\n        )\n        db.add(news)\n        db.commit()\n        db.refresh(news)\n        return news\n\n    @staticmethod\n    def update(db: Session, news: News, **data) -> News:\n        for field, value in data.items():\n            if value is not None:\n                setattr(news, field if field != \"published_at\" else \"published_at\", value)\n        news.updated_at = datetime.utcnow()\n        db.add(news)\n        db.commit()\n        db.refresh(news)\n        return news\n\n    @staticmethod\n    def delete(db: Session, news: News) -> None:\n        db.delete(news)\n        db.commit()\n*** End Patch```  #-}

