from fastapi import APIRouter
from models import Good, GoodBillet, Customer, CustomerBillet, Order, OrderBillet
from database import db, goods, orders, customers
from typing import List

router = APIRouter()


# =============================================
# = Create simple fake goods for initial test =
# =============================================
# @router.get("/goods/{amt}")
# async def create_goods(amt: int):
#     for i in range(1, amt + 1):
#         query = goods.insert().values(name=f'a_good{i}',
#                                       description=f'=={i**4}=='
#                                                   f'Lorem  ipsum  dolor  sit amet, '
#                                                   f'consectetur  adipiscing  elit. '
#                                                   f'Vestibulum    sagittis   dolor '
#                                                   f'mauris,  at  elementum  ligula '
#                                                   f'tempor  eget.'
#                                                   f'=={i**4}==',
#                                       price=round(i ** 2 / (i * 2) + i ** 2 / i ** 3, 2),
#                                       )
#         await db.execute(query)
#     return {'message': f'{amt} fake goods created'}
# ========================================


@router.post("/goods/", response_model=Good)
async def add_good(good: GoodBillet):
    query = goods.insert().values(**good.dict())
    last_id = await db.execute(query)
    return {**good.dict(), "id": last_id}


@router.get("/goods/", response_model=List[Good])
async def read_goods():
    query = goods.select()
    return await db.fetch_all(query)


@router.get("/goods/{good_id}", response_model=Good)
async def read_good(good_id: int):
    query = goods.select().where(goods.c.id == good_id)
    return await db.fetch_one(query)


@router.put("/goods/{good_id}", response_model=Good)
async def update_good(good_id: int, new_good: GoodBillet):
    query = goods.update().where(goods.c.id == good_id).values(**new_good.dict())
    await db.execute(query)
    return {**new_good.dict(), "id": good_id}


@router.delete("/goods/{good_id}")
async def delete_good(good_id: int):
    query = goods.delete().where(goods.c.id == good_id)
    await db.execute(query)
    return {"message": "A good deleted"}