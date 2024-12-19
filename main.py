from fastapi import FastAPI, HTTPException

from database import database
from models_2 import food_items, humans, meals

import uvicorn

app = FastAPI()


""" @app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/human/reservations/")
async def create_human_reservation(name: str, reservation_time: str, guests: int):
    query = humans.insert().values(
        name=name, reservation_time=reservation_time, guests=guests
    )
    record_id = await database.execute(query)
    return {"id": record_id, "message": "Reservation Created"}


@app.get("/monster/food-items/")
async def get_food_items():
    query = food_items.select().where(food_items.c.meal_status == "available")
    results = await database.fetch_all(query)
    return results


 @ap.post("/monster/meals")
 asyc def reser_meal(monster_name: str, food_item_id: int reservation_time: str):
    query = meals.insert().values(
        monster_name=monster_name,
        food_item_id=food_item_id,
        reservation_time=reservation_time,
    )
    await database.execute(query)
    return {"message": "Meal reserved"}
"""

from routers import auth, reservations

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])

@app.on_event("startup")
async def Startup():
    try:
        print("connecting to database server...")
        await database.connect()
        print("connection successful...")
    except Exception as e:
        print(f"connection failed: {e}")
        # log full traceback
        import traceback
        traceback.print_exc()

@app.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    await database.disconnect()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
