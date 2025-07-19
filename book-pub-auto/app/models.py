from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Revision(Base):
    __tablename__ = 'revisions'
    id = Column(Integer, primary_key=True)
    chapter_id = Column(Integer)
    version = Column(Integer)
    content = Column(Text)
    author_type = Column(String)  # 'human' or 'ai'
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine("sqlite:///revisions.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
