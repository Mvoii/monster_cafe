from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database import database
from sqlalchemy import text
from routers.auth import get_current_user


router = APIRouter()


class HumanReservation(BaseModel):
    name: str
    reservation_time: datetime
    guests: int


class MonsterReservation(BaseModel):
    monster_name: str
    food_item_id: int
    reservation_time: datetime


@router.post("/human-reservation")
async def create_human_reservation(
        reservation: HumanReservation,
        current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "human":
        raise HTTPException(status_code=403, detail="humans only")

    query = text("""
                WITH inserted_human AS (
                    INSERT INTO humans (name, reservation_time, guests)
                    VALUES (:name, :reservation_time, :guests)
                    RETURNING id
                )
                INSERT INTO food_items (human_id, food_type, meal_status)
                SELECT id, "human", "available" FROM inserted_human
    """)

    await database.execute(query=query, values={
                           "name": reservation.name,
                           "reservation_time": reservation.reservation_time,
                            "guests": reservation.guests
    })

    return {"message": "Human reservations created successfully"}


@router.post("/monster-reservation")
async def create_monster_reservation(
        reservation: MonsterReservation,
        current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "monster":
        raise HTTPException(status_code=400, detail="yeah, your lost, try the other section")

    availability_query = text("SELECT * FROM food_items WHERE id = :food_item_id AND meal_status = 'available'")
    available_item = await database.fetch_one(query=availability_query, values={"food_item_id": reservation.food_item_id})

    if not available_item:
        raise HTTPException(status_code=400, detail="selected item is not vailable")

    query = text("""
                 WITH updated_food_items AS (
                    UPDATE food_items
                    SET meal_status = 'reserved'
                    WHERE id = :food_item_id
                    RETURNING id
                )
                INSERT INTO meals (monster_name, food_item_id, reservation_time)
                SELECT :monster_name, id, :reservation_time FROM updated_food_items
            """)

    await database.execute(query=query, values={
                           "monster_name": reservation.monster_name,
                           "food_item_id": reservation.food_item_id,
                           "reservation_time": reservation.reservation_time
    })

    return {"message": "Dear monster, your reservation is successful"}

@router.get("/available-meals")
async def get_available_meals(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "monster":
        raise HTTPException(status_code=403, detail="Ariana, What are you doing here?")

    query = text("""
                 SELECT f.id, h.name, h.guests, h.reservation_time
                 FROM food_items f
                 JOIN humans h ON f.human_id = h.id
                 WHERE f.meal_status = "available"
    """)

    available_meals = await database.fetch_all(query=query)
    return available_meals
