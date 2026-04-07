from pathlib import Path

from omegaconf import OmegaConf

from app.conf.meta_config import MetaConfig
from app.entities.column_info import ColumnInfo
from app.entities.table_info import TableInfo
from app.models.column_info_mysql import ColumnInfoMySQL
from app.models.table_info_mysql import TableInfoMySQL
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository


class MetaKnowledgeService:
    def __init__(self,
                 meta_mysql_repository: MetaMySQLRepository,
                 dw_mysql_repository: DWMySQLRepository):
        self.meta_mysql_repository: MetaMySQLRepository = meta_mysql_repository
        self.dw_mysql_repository: DWMySQLRepository = dw_mysql_repository

    async def build(self, config_path: Path):
        # 1. 读取配置文件
        context = OmegaConf.load(config_path)
        schema = OmegaConf.structured(MetaConfig)
        meta_config: MetaConfig = OmegaConf.to_object(OmegaConf.merge(schema, context))

        # 2. 根据配置文件同步指定的表信息
        if meta_config.tables:
            table_infos: list[TableInfo] = []
            column_infos: list[ColumnInfo] = []
            # 2.1 将表信息和字段信息保存meta数据库中
            for table in meta_config.tables:
                # table -> table_info
                table_info = TableInfo(id=table.name,
                                       name=table.name,
                                       role=table.role,
                                       description=table.description)
                table_infos.append(table_info)

                # 查询字段类型
                column_types = await self.dw_mysql_repository.get_column_types(table.name)

                for column in table.columns:
                    # 查询字段取值示例
                    column_values = await self.dw_mysql_repository.get_column_values(table.name, column.name)
                    # column -> column_info
                    column_info = ColumnInfo(id=f"{table.name}.{column.name}",
                                             name=column.name,
                                             type=column_types[column.name],
                                             role=column.role,
                                             examples=column_values,
                                             description=column.description,
                                             alias=column.alias,
                                             table_id=table.name)
                    column_infos.append(column_info)

            async with self.meta_mysql_repository.session.begin():
                self.meta_mysql_repository.save_table_infos(table_infos)
                self.meta_mysql_repository.save_column_infos(column_infos)

            # 2.2 对字段信息建立向量索引

            # 2.3 对指定的维度字段取值建立全文索引

        # 3. 根据配置文件同步指定的指标信息
        if meta_config.metrics:
            pass
            # 3.1 将指标信息保存meta数据库中

            # 3.2 对指标信息建立向量索引
