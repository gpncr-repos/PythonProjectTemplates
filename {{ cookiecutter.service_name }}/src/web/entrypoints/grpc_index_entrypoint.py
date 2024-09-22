from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from tools.di_containers import stub_di_container

router = APIRouter(tags=["index"])


@router.get("/")
@inject
async def index(
    index_service_stub: ... = Depends(
        Provide[stub_di_container.IndexStubContainer.stub]
    ),
    index_service_response: ... = Depends(
        Provide[stub_di_container.IndexStubContainer.response]
    )
) -> str:
    response = index_service_stub.GetInfo(index_service_response)

    return f"{response.project_name} - {response.app_name} {response.app_version}"
