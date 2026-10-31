from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_session

from response_models import AppException, SuccessResponse

from models import User,Event,Category
from schemas import EventCreateSchema, EventSchema

event_router = APIRouter(prefix="/event",tags=["event"],dependencies=[Depends(get_current_user)])

@event_router.post("/create",response_model=SuccessResponse,status_code=201)
async def create_event(event_create_schema:EventCreateSchema,session:AsyncSession=Depends(get_session),user:User=Depends(get_current_user)):
    if len(event_create_schema.name)>30:
        raise AppException(code="EVENT_NAME_ERROR",status_code=400,message="O tamanho do nome do evento excede o limite de 30 caracteres")
    if len(event_create_schema.description)>512:
        raise AppException(code="EVENT_DESCRIPTION_ERROR",status_code=400,message="O tamanho da descrição do evento excecde o limite de 512 caracteres")
    category_result = await session.execute(select(Category).where(Category.id==event_create_schema.category_id))
    category = category_result.scalar_one_or_none()
    if category is None:
        raise AppException(code="EVENT_CATEGORY_ERROR",status_code=400,message="A categoria inserida não corresponde a nenhuma categoria salva")
    new_event = Event(
        name=event_create_schema.name,
        description=event_create_schema.description,
        done=event_create_schema.done,
        user_id=user.id,
        date=event_create_schema.date,
        time=event_create_schema.time,
        category_id=event_create_schema.category_id
    )
    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)
    return  {
        "success":True,
        "message": "Evento criado com sucesso",
        "data": {
            "event_id": new_event.id,
            "event_name":new_event.name
        }
    }

@event_router.get("/get",response_model=SuccessResponse,status_code=200)
async def get_event(event_id:int,session:AsyncSession=Depends(get_session),user:User=Depends(get_current_user)):
    event_result = await session.execute(select(Event).where(Event.id==event_id))
    event = event_result.scalar_one_or_none()
    if event is None:
        raise AppException(code="EVENT_NOT_FOUND", message=f"Não foi possível encontra envento de id {event_id}",status_code=400)

    if event.user_id!=user.id:
        raise AppException(code="ACCESS_DENIED",status_code=401,message="Acesso negado, você não pode verificar este evento")

    event_response = EventSchema.model_validate(event)
    return {
        "success":True,
        "Message":"Evento encontrado com sucesso",
        "data":event_response
    }