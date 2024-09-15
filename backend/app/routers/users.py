# Stub file - can extend if needed to sync user info from the Frontend API
from fastapi import APIRouter

# Define the router object
# router = APIRouter()



import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

# URL of the Frontend API where users are registered
FRONTEND_USERS_URL = "http://frontend_api:8000/users/"

@router.get("/admin/users/")
def get_users_from_frontend():
    try:
        # Make a request to the Frontend API to get users
        response = requests.get(FRONTEND_USERS_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve users from frontend")
        
        # Return the list of users from the Frontend API
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users from frontend: {e}")


@router.post("/users/")
def create_user(email: str, first_name: str, last_name: str):
    return {"email": email, "first_name": first_name, "last_name": last_name}
