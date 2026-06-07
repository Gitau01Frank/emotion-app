from sqlalchemy import (create_engine, Column, Integer,
                         String, Text, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./emotion.db")

engine       = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush  = False,
    bind       = engine
)
Base = declarative_base()

# Tables
class Message(Base):
    __tablename__ = "messages"

    id               = Column(Integer,  primary_key=True, index=True)
    text_content     = Column(Text,     nullable=False)
    detected_emotion = Column(String,   nullable=True)
    gpt_response     = Column(Text,     nullable=True)
    timestamp        = Column(DateTime, default=datetime.utcnow)

class EmotionLog(Base):
    __tablename__ = "emotion_log"

    id               = Column(Integer,  primary_key=True, index=True)
    detected_emotion = Column(String,   nullable=False)
    timestamp        = Column(DateTime, default=datetime.utcnow)

# Create tables 
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created ✅")

# Save message and log 
def save_message(text, emotion, gpt_response):
    db  = SessionLocal()
    try:
        msg = Message(
            text_content     = text,
            detected_emotion = emotion,
            gpt_response     = gpt_response,
            timestamp        = datetime.utcnow()
        )
        db.add(msg)

        log = EmotionLog(
            detected_emotion = emotion,
            timestamp        = datetime.utcnow()
        )
        db.add(log)
        db.commit()
        db.refresh(msg)
        return msg
    finally:
        db.close()

# Get recent messages
def get_all_messages(limit=50):
    db = SessionLocal()
    try:
        return db.query(Message)\
                 .order_by(Message.timestamp.desc())\
                 .limit(limit).all()
    finally:
        db.close()

# Get emotion counts
def get_emotion_counts():
    db = SessionLocal()
    try:
        logs   = db.query(EmotionLog).all()
        counts = {}
        for log in logs:
            emotion = log.detected_emotion
            counts[emotion] = counts.get(emotion, 0) + 1
        return counts
    finally:
        db.close()

# Get emotion trend
def get_emotion_trend():
    db = SessionLocal()
    try:
        logs = db.query(EmotionLog)\
                 .order_by(EmotionLog.timestamp.asc()).all()
        return [
            {
                "date"   : log.timestamp.strftime("%Y-%m-%d"),
                "emotion": log.detected_emotion
            }
            for log in logs
        ]
    finally:
        db.close()