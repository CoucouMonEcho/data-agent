import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker

from app.conf.app_config import DBConfig, app_config


class MySQLClientManager:
    def __init__(self, config: DBConfig):
        self._engine: AsyncEngine | None = None
        self.session_factory = None
        self._config = config

    def _get_url(self):
        return f"mysql+asyncmy://{self._config.user}:{self._config.password}@{self._config.host}:{self._config.port}/{self._config.database}?charset=utf8mb4"

    def init(self):
        self._engine = create_async_engine(self._get_url(), pool_size=10, pool_pre_ping=True)
        self.session_factory = async_sessionmaker(self._engine, autoflush=True, expire_on_commit=False)

    async def close(self):
        await self._engine.dispose()


# Base.metadata.create_all(engine)
meta_mysql_client_manager = MySQLClientManager(app_config.db_meta)
dw_mysql_client_manager = MySQLClientManager(app_config.db_dw)

if __name__ == '__main__':
    dw_mysql_client_manager.init()


    async def test():
        async with dw_mysql_client_manager.session_factory() as session:
            sql = "select * from fact_order limit 10"
            result = await session.execute(text(sql))

            rows = result.mappings().fetchall()

            print(type(rows))
            print(type(rows[0]))
            print(rows[0]['order_id'])


    asyncio.run(test())
