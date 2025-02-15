from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import pymysql
import time
import os
from dotenv import load_dotenv

load_dotenv() 

app = FastAPI()

while True:
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        print("Connected to database")
        break
    except Exception as error:
        print("Error while connecting to database", error)
        time.sleep(2)
        

class PostValidation(BaseModel):
    name: str
    email: str


@app.get("/")
def root():
    return {"Hello Pranjal"}


@app.get("/users")
def get_users():
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    return {"data": all_users}


@app.post("/users",  status_code = status.HTTP_201_CREATED)
def create_user(payload: PostValidation):
    # This %s are placeholders for the values of title, content and published and protects us from SQL injection
    cursor.execute("INSERT INTO users (name, email) VALUES ( %s, %s)", (payload.name, payload.email))
    # Commit the changes to the database
    conn.commit()
    # Fetch the last inserted post
    cursor.execute("SELECT * FROM users WHERE id = LAST_INSERT_ID()")
    new_user = cursor.fetchone()
    return {"new user is": new_user}


@app.get("/users/{id}")
def get_user(id: int):
    cursor.execute("SELECT * FROM users WHERE id = %s", (str(id),))
    selected_user = cursor.fetchone()
    # If id is not found in our database, raise an exception
    if not selected_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")
    return {f"User is ": selected_user}


@app.delete("/users/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    cursor.execute("DELETE FROM users WHERE id = %s", (str(id),))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/users/{id}", status_code = status.HTTP_202_ACCEPTED)
def update_user(id: int, payload: PostValidation):
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (payload.name, payload.email, str(id)))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE id = %s", (str(id),))
    updated_user = cursor.fetchone()
    if cursor.rowcount == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    return {"message": updated_user}