from sqlalchemy import Column, Integer, String

from databases import Base


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title = Column(String, index=True, nullable=False)
    ingredients = Column(String, index=True)
    desc = Column(String, index=True)
    coocking_time = Column(Integer, index=True)
    count = Column(Integer, default=0)
