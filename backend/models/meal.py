from sqlalchemy import Column, Integer, String
from backend.database import Base

class Meal(Base): 
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients = Column(String) 
    calories = Column(Integer)
    protein = Column(Integer) 
    fat = Column(Integer)
    carbs = Column(Integer) 
    