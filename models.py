from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(Integer, nullable=False)

class HabitType(Base):
    __tablename__ = 'habit_type'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    frequency = Column(Integer, nullable=False)

class Habit(Base):
    __tablename__ = 'habit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(Integer, nullable=False)
    fk_user = Column(Integer, ForeignKey('user.id'), nullable=False)
    fk_habit_type = Column(Integer, ForeignKey('habit_type.id'), nullable=False)

    user = relationship("User")
    habit_type = relationship("HabitType")

    def __repr__(self):
        created_at_formatted = datetime.fromtimestamp(self.created_at).strftime('%d-%m-%Y')
        return f"Habit(id={self.id}, title={self.title}, description={self.description}, created_at={created_at_formatted}, fk_user={self.fk_user}, fk_habit_type={self.fk_habit_type})"

class HabitTracking(Base):
    __tablename__ = 'habit_tracking'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fk_habit = Column(Integer, ForeignKey('habit.id'), nullable=False)
    checked_at = Column(Integer, nullable=False)

    habit = relationship("Habit")

# To create all tables in the engine.
# Base.metadata.create_all(engine)
