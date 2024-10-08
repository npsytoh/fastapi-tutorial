from typing import List
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session

from . import models
from . import schemas
from . import crud
from .database import SessionLocal
from .database import engine


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Read
@app.get('/users', response_model=List[schemas.User])
async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get('/rooms', response_model=List[schemas.Room])
async def read_rooms(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    room = crud.get_rooms(db, skip=skip, limit=limit)
    return room

@app.get('/bookings', response_model=List[schemas.Booking])
async def read_bookings(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings


# Create
@app.post('/users', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post('/rooms', response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)

@app.post('/bookings', response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)

