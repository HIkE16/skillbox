from fastapi import FastAPI
from sqlalchemy import update
from sqlalchemy.future import select

import models
import schemas
from databases import engine, session

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post("/recipes", response_model=schemas.RecipeOut)
async def recipe_post(recipe: schemas.RecipeIn) -> models.Recipe:
    """
    Сервис добавляет рецепт в БД

    :params:
    - **title: string** | Название рецепта
    - **ingredients: string** | Перечень ингредиентов
    - **desc: string** | Описание рецепта
    - **coocking_time: int** | Время приготовление в минутах
    """
    new_recipe = models.Recipe(**recipe.model_dump())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe


@app.get("/recipes", response_model=list[schemas.RecipeAll])
async def recipe_get() -> list[models.Recipe]:
    """
    Сервис возвращает список рецептов с БД
    """
    res = await session.execute(
        select(models.Recipe).order_by(
            models.Recipe.count.desc(), models.Recipe.coocking_time.desc()
        )
    )
    return list(res.scalars().all())


@app.get("/recipes/{id}", response_model=schemas.RecipeId)
async def recipe_get_by_id(id: int):
    """
    Сервис возвращает рецепт с БД по ID

    :params:
    - **id: int** ID - рецепта
    """
    res = await session.execute(select(models.Recipe).where(models.Recipe.id == id))
    result = res.scalars().one_or_none()
    if result is not None:
        await session.execute(
            update(models.Recipe)
            .where(models.Recipe.id == id)
            .values(count=result.count + 1)
        )
        return result
    return {"error": "Рецепт не найден"}