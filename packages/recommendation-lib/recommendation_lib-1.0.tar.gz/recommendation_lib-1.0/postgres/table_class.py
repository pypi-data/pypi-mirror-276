from sqlalchemy import Column, Integer, String, Float, DateTime, Sequence, Text
from sqlalchemy.ext.declarative import declarative_base


# Define a base class for declarative class definitions
Base = declarative_base()

# Define your table classes
class Machines(Base):
    __tablename__ = 'machines'

    content_id = Column(String, primary_key=True)
    machine_name = Column(String)
    os = Column(String)
    user_points = Column(Integer)
    root_points = Column(Integer)
    total_points = Column(Integer)
    difficulty = Column(String)
    description = Column(Text)
    variety = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class MachineRatings(Base):
    __tablename__ = 'machine_ratings'
    id = Column(Integer, Sequence('id'), primary_key=True)
    machine_name = Column(String)
    message = Column(String)
    created_at = Column(DateTime)
    user_rating = Column(Integer)
    difficulty = Column(String)
    avg_rating = Column(Float)

class ContentOwns(Base):
    __tablename__ = 'content_owns'

    content_own_id = Column(String(250), primary_key=True)
    content_id = Column(String(250))
    content_name = Column(String(50))
    points = Column(Integer)
    difficulty = Column(String(50))
    own_type = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_uuid = Column(String(250))