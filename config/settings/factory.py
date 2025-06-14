from dependency_injector import containers, providers

from .databases import (
    BaseDatabaseSettings,
    DBEngineEnum,
    DjangoDatabases,
    PostgresDatabaseSettings,
    SqliteDatabaseSettings,
)


class DbContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db_factory = providers.FactoryAggregate(
        {
            DBEngineEnum.SQLITE: providers.Factory(SqliteDatabaseSettings),
            DBEngineEnum.POSTGRES: providers.Factory(PostgresDatabaseSettings),
        }
    )
    fct = providers.Factory(db_factory, config.engine)
    django_databases = providers.Singleton(
        DjangoDatabases,
        default=fct,
    )


def get_django_dbs() -> DjangoDatabases:
    """Get the Django database settings."""
    db_container = DbContainer()
    db_container.config.from_pydantic(BaseDatabaseSettings())
    return db_container.django_databases()


def get_django_db_dict() -> dict:
    """Get the Django database settings as a dictionary."""
    db = get_django_dbs()
    return db.model_dump(mode="json", by_alias=True)
