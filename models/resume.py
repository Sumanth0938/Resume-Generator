from sqlalchemy import Column, Integer, JSON,String
from infra.database import Base

class Resume(Base):
    __tablename__ = 'resume'

    id = Column(Integer,primary_key=True)
    username = Column(String)
