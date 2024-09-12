from fastapi import APIRouter

from models.dto import cluster_domain_dto
from services import oil_rate_calc_service
from web.schemas import oil_rate_calculator_schema

router = APIRouter(prefix="/cluster")


@router.post("/calc-oil-rate")
async def calc_cluster_oil_rate(
    calc_data: oil_rate_calculator_schema.ClusterSchema
) -> oil_rate_calculator_schema.ClusterOilRate:
    """
    Рассчитать дебит нефти для куста скважин
    :param calc_data: исходные данные для расчета дебита нефти куста скважин
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

    calc_service = oil_rate_calc_service.OilRateCalcService(geology_params, wells)

    result = calc_service()

    return oil_rate_calculator_schema.ClusterOilRate(oil_rate=result)