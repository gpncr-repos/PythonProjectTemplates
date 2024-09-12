from interfaces import base_factory
from models.domain.cluster import aggregates, entities, value_objects
from models.dto import cluster_domain_dto


class GeologyPropertiesFactory(base_factory.BaseFactory):
    """
    Фабрика объектов геологических свойств пласта
    """

    def create(self, params: cluster_domain_dto.GeologyPropertiesDTO) -> value_objects.GeologyProperties:
        """
        Создать объект геологических свойств пласта
        :param params: параметры пласта
        :return: объект свойств
        """

        return value_objects.GeologyProperties(
            permeability=params.permeability,
            thickness=params.thickness,
            layer_pressure=params.layer_pressure,
            supply_contour_radius=params.supply_contour_radius,
            oil_viscosity=params.oil_viscosity
        )


class WellFactory(base_factory.BaseFactory):
    """
    Фабрика объектов скважин
    """

    def create(self, params: cluster_domain_dto.WellPropertiesDTO) -> entities.Well:
        """
        Создать объект скважины
        :param params: параметры скважины
        :return: объект свойств
        """

        return entities.Well(
            id_=params.id_,
            name=params.name,
            wellbore_pressure=params.wellbore_pressure,
            radius=params.radius
        )


class ClusterFactory(base_factory.BaseFactory):
    """
    Фабрика агрегатов Кустов
    """

    def create(self, params: value_objects.GeologyProperties) -> aggregates.Cluster:
        """
        Создать объект Куста
        :param params: геологические свойства
        :return: объект Куста
        """

        return aggregates.Cluster(params)
