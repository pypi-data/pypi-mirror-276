from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()
# from models import Base

class SocialMediaPostEmbedding(Base):
    __tablename__ = 'kepler_pg_vector'

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    post = Column(Text)
    post_date = Column(Text)
    cleanedpost = Column(Text)
    textembedding = Column(Vector(384))
