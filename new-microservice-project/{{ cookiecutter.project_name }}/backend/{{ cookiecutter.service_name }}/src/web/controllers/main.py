from fastapi import APIRouter

from config.settings import settings

router = APIRouter(prefix="/api", tags=["main"])


@router.get("/")
def index() -> str:
    return f"{settings.product_name} - {settings.service_name}"


@router.get("/version")
def get_version() -> str:
    return f"{settings.service_name} - {settings.service_version}"
