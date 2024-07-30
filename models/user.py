from sqlalchemy import Column, Integer, String,ForeignKey
from infra.database import Base
from models.resume import Resume


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)
    location=Column(String)
    country = Column(String)
    mobile_number=Column(String)
    resume_id = Column(Integer,ForeignKey('resume.id'))

