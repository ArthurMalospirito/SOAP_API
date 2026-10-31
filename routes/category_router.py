from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_session,verify_admin

from response_models import AppException, SuccessResponse

from models import User,Category
from schemas import CategoryCreateSchema, CategorySchema

category_router = APIRouter(prefix="/category",tags=["category"],dependencies=[Depends(get_current_user)])

@category_router.post("/create",response_model=SuccessResponse,status_code=201)
async def create_category(category_create_schema:CategoryCreateSchema,session:AsyncSession=Depends(get_session),user:User = Depends(verify_admin)):
    if len(category_create_schema.name)>30:
        raise AppException(code="CATEGORY_NAME_ERROR",message="O nome da categoria excede o limite de 30 caracteres",status_code=400)
    if len(category_create_schema.description)>512:
        raise AppException(code="CATEGORY_DESCRIPTION_ERROR",message="A descrição da categoria excede o limite de 512 caracteres",status_code=400)

    new_category = Category(
        name=category_create_schema.name,
        description=category_create_schema.description,
        priority=category_create_schema.priority,
        color=category_create_schema.color
    )
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return {
        "success":True,
        "message":"Categoria criada com sucesso",
        "data": {
            "category_id":new_category.id,
            "category_name":new_category.name
        }
    }

@category_router.get("/get",response_model=SuccessResponse,status_code=200)
async def get_category(category_id:int,session:AsyncSession=Depends(get_session)):
    category_result = await session.execute(select(Category).where(Category.id==category_id))
    category = category_result.scalar_one_or_none()
    if category is None:
        raise AppException(code="CATEGORY_NOT_FOUND",message=f"A categoria de id {category_id} não foi encontrada",status_code=400)

    category_response = CategorySchema.model_validate(category)
    return {
        "success":True,
        "message":"Categoria encontrada com sucesso",
        "data": category_response
    }