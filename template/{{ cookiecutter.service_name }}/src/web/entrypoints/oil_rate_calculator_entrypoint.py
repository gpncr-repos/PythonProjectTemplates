from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends

from interfaces import base_factory
from models.dto import cluster_domain_dto
from tools import di_container
from web.schemas import oil_rate_calculator_schema

router = APIRouter(prefix="/cluster")


@router.post("/oil-rate")
@inject
async def calc_cluster_oil_rate(
    calc_data: oil_rate_calculator_schema.ClusterSchema,
    calc_service_factory: base_factory.BaseFactory = Depends(Provide[di_container.ServiceContainer])
) -> oil_rate_calculator_schema.ClusterOilRate:
    """
    Рассчитать дебит нефти для куста скважин
    :param calc_data: исходные данные для расчета дебита нефти куста скважин
    :param calc_service_factory: фабрика сервисов расчетов дебита куста скважин
    :return: дебит нефти куста скважин
    """

    geology_params = cluster_domain_dto.GeologyPropertiesDTO(
        permeability=calc_data.geology_params.permeability,
        thickness=calc_data.geology_params.thickness,
        layer_pressure=calc_data.geology_params.layer_pressure,
        supply_contour_radius=calc_data.geology_params.supply_contour_radius,
        oil_viscosity=calc_data.geology_params.oil_viscosity
    )
    wells = [
        cluster_domain_dto.WellPropertiesDTO(
            id_=well.id_,
            name=well.name,
            wellbore_pressure=well.wellbore_pressure,
            radius=well.radius
        )
        for well in calc_data.wells
    ]

    calc_service = calc_service_factory.create(geology_params, wells)

    result = calc_service.calculate_cluster_oil_rate()

    return oil_rate_calculator_schema.ClusterOilRate(oil_rate=result)