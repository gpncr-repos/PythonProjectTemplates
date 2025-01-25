import datetime
import uuid
from typing import Iterable

from models.domain.cluster import entities, root, value_objects
from repositories import asyncpg_repository


class ClusterRepository(asyncpg_repository.AsyncpgRepository):
    """
    Репозиторий для работы с агрегатом Куст
    """

    async def create(self) -> None:
        await super().create()

    async def retrieve(
        self,
        id_: uuid.UUID,
        dt: datetime.datetime
    ) -> root.Cluster:
        """
        Получить данные для инициализации объекта куста
        :param id_: идентификатор куста
        :param dt: время замера
        :return: модель домена
        """

        query_cluster = """
            with geology as (
                select
                    id,
                    permeability,
                    thickness,
                    layer_pressure,
                    supply_contour_radius,
                    oil_viscosity,
                    dt,
                    cluster_id
                from geology_params
                where
                    dt <= $1
                    and cluster_id = $2
            )
            select
                c.id,
                c.name,
                g.permeability,
                g.thickness,
                g.layer_pressure,
                g.supply_contour_radius,
                g.oil_viscosity,
                g.dt
            from cluster c
            left join geology g
            on c.id = g.cluster_id
            where c.id = $2
        """

        query_wells = """
            with history as (
                select
                    wellbore_pressure,
                    dt,
                    well_id,
                    row_number() over(partition by well_id order by dt) row_num
                from well_stats_history
                where dt <= $1
            )
            select
                w.id,
                w.name,
                w.radius,
                h.wellbore_pressure,
                h.dt
            from well w
            left join history h
                on h.well_id = w.id
            where w.cluster_id = $2
                and h.row_num = 1
        """

        connection = await self._get_connection()
        cursor = connection.cursor

        cluster = await cursor.fetchrow(query_cluster, dt, str(id_))
        wells = await super().list(query_wells, params=[dt, str(id_)])

        domain_cluster = root.Cluster(
            id_=id_,
            name=cluster["name"],
            geology_params=value_objects.GeologyProperties(
                permeability=cluster["permeability"],
                thickness=cluster["thickness"],
                layer_pressure=cluster["layer_pressure"],
                supply_contour_radius=cluster["supply_contour_radius"],
                oil_viscosity=cluster["oil_viscosity"]
            )
        )

        domain_wells = [
            entities.Well(
                id_=well["id"],
                name=well["name"],
                wellbore_pressure=well["wellbore_pressure"],
                radius=well["radius"]
            ) for well in wells
        ]

        for well in domain_wells:
            domain_cluster.add_well(well)

        return domain_cluster

    async def delete(self) -> None:
        await super().delete()

    async def update(self) -> None:
        await super().update()

    async def list(
        self, query: str, rows_count: int | None = None, params: list | None = None
    ) -> Iterable[tuple]:
        raise NotImplementedError
