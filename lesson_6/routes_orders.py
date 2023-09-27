from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from models import Order, OrderBillet, OrderResponse
from database import db, orders, customers, goods
from typing import List

router = APIRouter()


@router.post("/orders/", response_model=Order)
async def add_order(order: OrderBillet):
    query = orders.insert().values(**order.dict())
    last_id = await db.execute(query)
    return {**order.dict(), "id": last_id}


@router.get("/orders/", response_model=List[OrderResponse])
async def read_orders():
    query = (
        select(
            [
                orders.c.customer_id,
                orders.c.good_id,
                customers.c.id,
                goods.c.id,
                orders.c.order_date,
                orders.c.status,
                customers.c.name,
                customers.c.surname,
                customers.c.email,
                goods.c.name,
                goods.c.price,
            ]
        )
            .join(customers, orders.c.customer_id == customers.c.id)
            .join(goods, orders.c.good_id == goods.c.id)
    )

    response = await db.fetch_all(query)
    if response:
        return [
            OrderResponse(
                order_date=r[4],
                status=r[5],
                name=r[6],
                surname=r[7],
                email=r[8],
                good_name=r[9],
                price=r[10],
            )
            for r in response
        ]

    raise HTTPException(404, {"message": "Not found"})


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def read_order(order_id: int):
    query = (
        select(
            [
                orders.c.customer_id,
                orders.c.good_id,
                customers.c.id,
                goods.c.id,
                orders.c.order_date,
                orders.c.status,
                customers.c.name,
                customers.c.surname,
                customers.c.email,
                goods.c.name,
                goods.c.price,
            ]
        )
            .join(customers, orders.c.customer_id == customers.c.id)
            .join(goods, orders.c.good_id == goods.c.id)
            .where(orders.c.id == order_id)
    )
    response = await db.fetch_one(query)

    if response:
        result = OrderResponse(
            order_date=response[4],
            status=response[5],
            name=response[6],
            surname=response[7],
            email=response[8],
            good_name=response[9],
            price=response[10],
        )
        return result
    raise HTTPException(404, {"message": "Not found"})


@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderBillet):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await db.execute(query)
    return {**new_order.dict(), "id": order_id}


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {"message": "A order deleted"}