from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

metadata = MetaData()

humans = Table(
    "humans",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("reservation_time", TIMESTAMP, nullable=False),
    Column("guests", Integer, nullable=False),
)

food_items = Table(
    "food_items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("human_id", Integer, ForeignKey("humans.id")),
    Column("food_type", String, nullable=False),
    Column("meal_status", String, default="available"),
)

meals = Table(
    "meals",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("monster_name", String, nullable=False),
    Column("food_item_id", Integer, ForeignKey("food_items.id")),
    Column("reservation_time", TIMESTAMP, nullable=False),
)


