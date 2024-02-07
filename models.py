from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)

from db import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Person(Base):
    __tablename__ = 'person'

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(50))
    films: Mapped[str] = mapped_column(String(600))
    gender: Mapped[str] = mapped_column(String(10))
    hair_color: Mapped[str] = mapped_column(String(50))
    height: Mapped[int] = mapped_column(Integer)
    homeworld: Mapped[str] = mapped_column(String(200))
    mass: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(200))
    skin_color: Mapped[str] = mapped_column(String(50))
    species: Mapped[str] = mapped_column(String(600))
    starships: Mapped[str] = mapped_column(String(600))
    vehicles: Mapped[str] = mapped_column(String(600))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

