from pydantic import BaseModel, Field


class GoodBillet(BaseModel):
    name: str = Field(..., max_length=20)
    description: str = Field(max_length=300)
    price: float = Field(...,)


class Good(GoodBillet):
    id: int