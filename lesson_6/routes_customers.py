from fastapi import APIRouter
from models import Customer, CustomerBillet, Order, OrderBillet
from database import db, orders, customers
from typing import List

router = APIRouter()


# =================================================
# = Create simple fake customers for initial test =
# =================================================
# @router.get("/customers/{amt}")
# async def create_customers(amt: int):
#     for i in range(1, amt + 1):
#         query = customers.insert().values(
#             name=f'Castor - {i}',
#             surname=f'Doe - {i}',
#             email=f'castor{i:0>4}@mail{i%5}.dom',
#             password=f'FakePassword{i^3}',
#         )
#         await db.execute(query)
#     return {'message': f'{amt} fake customers created'}
# ========================================


@router.post("/customers/", response_model=Customer)
async def add_customer(customer: CustomerBillet):
    query = customers.insert().values(**customer.dict())
    last_id = await db.execute(query)
    return {**customer.dict(), "id": last_id}


@router.get("/customers/", response_model=List[Customer])
async def read_customers():
    query = customers.select()
    return await db.fetch_all(query)


@router.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int):
    query = customers.select().where(customers.c.id == customer_id)
    return await db.fetch_one(query)


@router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, new_customer: CustomerBillet):
    query = customers.update().where(customers.c.id == customer_id).values(**new_customer.dict())
    await db.execute(query)
    return {**new_customer.dict(), "id": customer_id}


@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    query = customers.delete().where(customers.c.id == customer_id)
    await db.execute(query)
    return {"message": "A customer removed from base"}