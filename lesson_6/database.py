from databases import Database
from sqlalchemy import MetaData, Column, Integer, String, Table, Date, Float, create_engine, ForeignKey

from settings import settings

db = Database(settings.DATABASE_URL)

metadata = MetaData()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

goods = Table(
    "goods",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
    Column("price", Float, nullable=False),
)

customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("surname", String(50), nullable=False),
    Column("email", String(128), nullable=False),
    Column("password", String, nullable=False),
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey('goods.id'), nullable=False),
    Column("good_id", Integer, ForeignKey('goods.id'), nullable=False),
    Column("order_date", Date, nullable=False),
    Column("status", String, nullable=False),
)

metadata.create_all(engine)

"""
A code from documentation to FastAPI:

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
"""