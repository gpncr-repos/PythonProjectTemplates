# thirdparty
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

# project
from config.settings import Settings

router = APIRouter(prefix="/api", tags=["main"])


@router.get("/")
@inject
async def index(settings: FromDishka[Settings]) -> str:
    return f"{settings.product_name} - {settings.service_name}"


@router.get("/version")
@inject
async def get_version(settings: FromDishka[Settings]) -> str:
    return f"{settings.service_name} - {settings.service_version}"


