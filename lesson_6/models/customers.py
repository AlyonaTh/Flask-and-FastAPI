from pydantic import BaseModel, Field, EmailStr


class CustomerBillet(BaseModel):
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    email: EmailStr = Field(...,)
    password: str = Field(...,)


class Customer(CustomerBillet):
    id: int