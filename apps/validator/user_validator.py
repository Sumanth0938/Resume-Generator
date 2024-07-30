from pydantic import BaseModel,EmailStr

class UserModel(BaseModel):
    id:int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    location: str
    country: str
    mobile_number: str
   
