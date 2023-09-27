import uvicorn

from fastapi import FastAPI
from database import db
import routes_goods
import routes_customers
import routes_orders

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

app.include_router(routes_goods.router, tags=["Goods"])
app.include_router(routes_customers.router, tags=["Customers"])
app.include_router(routes_orders.router, tags=["Orders"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )