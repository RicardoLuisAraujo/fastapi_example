from fastapi import FastAPI, HTTPException
from models.models_def import User, Gender, Role
from uuid import uuid4, UUID

app = FastAPI()

db: list[User] = [
    User(
        id=uuid4(),
        first_name="Ricardo",
        last_name="Araújo",
        gender=Gender.male,
        roles=[Role.student],
    ),
    User(
        id=uuid4(),
        first_name="Sofia",
        last_name="Geraldo",
        gender=Gender.female,
        roles=[Role.admin, Role.user],
    ),
]


@app.get("/")
def root() -> dict:
    return {"message": "You can use the path /api/users to get all users."}


@app.get("/api/users")
async def get_users() -> list[User]:
    return db


@app.post("/api/users")
async def create_user(user: User) -> User:
    db.append(user)
    return user


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID) -> str:
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return "User deleted"
    raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")
