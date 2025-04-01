from sqlalchemy import Session
from backend.models.meal import Meal 

def create_meal(db:Session, name:str,ingredients:str,calories:int, protein:int,fat:int,carbs:int):
    meal = Meal(name=name,ingredients=ingredients,calories=calories,protein=protein,fat=fat,carbs=carbs)
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

def get_meals(db:Session):
    return db.query(Meal).all()

