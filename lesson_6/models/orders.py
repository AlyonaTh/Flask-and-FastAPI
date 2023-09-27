from pydantic import BaseModel, Field
from datetime import date


class OrderBillet(BaseModel):
    customer_id: int = Field(..., )
    good_id: int = Field(..., )
    order_date: date = Field(..., format="%Y-%m-%d")
    status: str = Field(..., )


class Order(OrderBillet):
    id: int


class OrderResponse(BaseModel):
    order_date: date
    status: str
    name: str
    surname: str
    email: str
    good_name: str
    price: str

    class Config:
        from_attributes = True  # в более ранних версиях orm_mode = True