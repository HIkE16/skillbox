from pydantic import BaseModel


class BaseRecipe(BaseModel):
    title: str
    ingredients: str
    desc: str
    coocking_time: int


class RecipeIn(BaseRecipe): ...


class RecipeOut(BaseRecipe):
    id: int
    count: int

    class Config:
        orm_mose = True


class RecipeAll(BaseModel):
    title: str
    count: int
    coocking_time: int

    class Config:
        orm_mose = True


class RecipeId(BaseModel):
    title: str
    coocking_time: int
    ingredients: str
    desc: str

    class Config:
        orm_mose = True
